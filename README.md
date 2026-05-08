Client → Route53 → API Gateway (with WAF) → Lambda → DynamoDB
                                    ↓
                                X-Ray Tracing
                                CloudWatch Logs
Project Structure

group5-url-shortener/
├── .github/
│   └── workflows/
│       └── terraform.yml       # The CI/CD pipeline script
├── src/
│   ├── create/
│   │   └── index.py            # Python code for POST /newurl
│   └── retrieve/
│       └── index.py            # Python code for GET /{shortid}
├── main.tf                     # Backend, Providers, and S3 Bucket
├── variables.tf                # Global variables (Group name, IP, etc.)
├── lambda.tf                   # Lambda functions and IAM roles
├── api_gateway.tf              # API Gateway resources and DNS
├── waf.tf                      # Web ACL and IP sets
├── .gitignore                  # Files to exclude from Git
└── README.md                   # Project documentation

                                
