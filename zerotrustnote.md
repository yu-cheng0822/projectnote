<img width="810" height="484" alt="image" src="https://github.com/user-attachments/assets/f0ab4b59-4bfb-4798-8d8a-40bca045edf7" />
<img width="824" height="434" alt="image" src="https://github.com/user-attachments/assets/175d81a5-1723-41e8-a6bb-dbfa93fac474" />


對比 3：Per-Request Authorization
NIST 原本使用的是：
Per-session / Per-resource
而你的 Agent Security 可以合理延伸為：
Per-Tool-Request Authorization
# 安全架構
      ProtectedAgent
                         │
                         │ Tool Request
                         ▼
              ┌────────────────────┐
              │ SecurityArchitecture│
              └─────────┬──────────┘
                        │
                Agent Identity
                        │
                        ▼
                Permission Check
                        │
                        ▼
                 Risk Assessment
                        │
                        ▼
                Behavior History
                        │
                        ▼
                 Dynamic Trust
                        │
                        ▼
                  Policy Engine
                   /          \
               ALLOW          DENY
                 │              │
                 └──────┬───────┘
                        ▼
                  Security Event
                        │
                        ▼
                Continuous Monitor
                        │
                        ▼
                  Trust Update
                        │
                        └─────────────┐
                                      │
                     Next Request ◄───┘
