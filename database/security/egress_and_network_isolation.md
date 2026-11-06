# Network Isolation & Egress Filtering Architecture (DLP Safeguards 13 & 14)

## Overview
This specification details the infrastructure and operating system boundary controls that prevent data exfiltration, lateral network movement, and untrusted outbound connections from the database and application runtime contexts.

---

## 1. SAFEGUARD 13: Network Isolation (Private Subnet & TLS Hardening)

### Architectural Design
1. **Zero Public Ingress:**
   - The PostgreSQL cluster is provisioned strictly within private application subnets (`10.0.1.0/24`, `10.0.2.0/24`).
   - No public IPv4/IPv6 addresses are assigned to database endpoints or replicas.
   - Administrative access is restricted to encrypted Bastion jump hosts or AWS Systems Manager (SSM) Session Manager.

2. **Strict Host-Based Authentication (`pg_hba.conf`):**
   ```ini
   # Reject all unencrypted TCP connections
   hostnossl   all             all             0.0.0.0/0               reject
   hostnossl   all             all             ::/0                    reject

   # Enforce TLS 1.3 with SCRAM-SHA-256 for private application subnets
   hostssl     kisan_setu_prod app_service     10.0.0.0/16             scram-sha-256 clientcert=verify-full
   hostssl     kisan_setu_prod app_audit       10.0.3.0/24             scram-sha-256 clientcert=verify-full
   hostssl     kisan_setu_prod app_rag_public  10.0.4.0/24             scram-sha-256 clientcert=verify-full

   # Deny everything else
   host        all             all             all                     reject
   ```

3. **PostgreSQL Server Network Configuration (`postgresql.conf`):**
   ```ini
   listen_addresses = '10.0.1.5'          # Bind strictly to internal private IP
   ssl = on
   ssl_cert_file = '/etc/ssl/certs/db-server.crt'
   ssl_key_file = '/etc/ssl/private/db-server.key'
   ssl_ca_file = '/etc/ssl/certs/internal-root-ca.pem'
   ssl_min_protocol_version = 'TLSv1.3'
   ssl_ciphers = 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384'
   password_encryption = 'scram-sha-256'
   ```

---

## 2. SAFEGUARD 14: Database & Application Egress Filtering

### Engine-Level Egress Prevention
PostgreSQL features that allow executing host-level processes or making arbitrary network sockets must be disabled or strictly firewalled:
1. **Disable Untrusted Language Extensions:**
   - Untrusted procedural languages (`plpythonu`, `plperlu`, `pltclu`) are strictly forbidden. Only standard trusted `plpgsql` is enabled.
2. **Revoke File & Program Execution Privileges:**
   ```sql
   REVOKE EXECUTE ON FUNCTION pg_read_file(text) FROM PUBLIC;
   REVOKE EXECUTE ON FUNCTION pg_read_file(text, bigint, bigint) FROM PUBLIC;
   REVOKE EXECUTE ON FUNCTION pg_read_binary_file(text) FROM PUBLIC;
   REVOKE EXECUTE ON FUNCTION pg_stat_file(text) FROM PUBLIC;
   REVOKE EXECUTE ON FUNCTION pg_ls_dir(text) FROM PUBLIC;
   ```
   The `COPY ... TO PROGRAM` and `COPY ... FROM PROGRAM` commands are strictly blocked for non-superusers.

### Host / Container Egress Filtering (Kubernetes NetworkPolicy)
The following NetworkPolicy blocks all egress traffic originating from the PostgreSQL cluster except for local DNS resolution, NTP synchronization, and authorized replica nodes.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgres-dlp-egress-lockdown
  namespace: kisan-database
spec:
  podSelector:
    matchLabels:
      app: kisan-setu-postgres
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Permit ingress ONLY from authorized backend API pods on port 5432
  - from:
    - namespaceSelector:
        matchLabels:
          name: kisan-backend
      podSelector:
        matchLabels:
          app: kisan-api
    ports:
    - protocol: TCP
      port: 5432
  egress:
  # 1. Allow DNS queries to internal CoreDNS only
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
  # 2. Allow replication traffic strictly to replica database pods
  - to:
    - podSelector:
        matchLabels:
          role: replica
    ports:
    - protocol: TCP
      port: 5432
  # All outbound connections to external public IPs (Internet) are DROP by default
```

### Linux Host Egress Filtering (`iptables`)
If running on virtual machines or bare-metal instances:
```bash
# Set default policy for OUTPUT chain to DROP
iptables -P OUTPUT DROP

# Allow loopback traffic
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections (replies to legitimate ingress queries)
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow internal DNS queries (10.0.0.2)
iptables -A OUTPUT -p udp -d 10.0.0.2 --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp -d 10.0.0.2 --dport 53 -j ACCEPT

# Allow internal NTP synchronization
iptables -A OUTPUT -p udp -d 10.0.0.123 --dport 123 -j ACCEPT

# Log any unauthorized outbound connection attempt for DAM / UEBA analysis
iptables -A OUTPUT -m limit --limit 5/min -j LOG --log-prefix "DB_EGRESS_BLOCKED: " --log-level 4
```
