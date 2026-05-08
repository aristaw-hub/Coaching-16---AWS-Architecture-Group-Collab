variable "group_name" {
  description = "Project group name used for resource naming"
  type        = string
  default     = "group5"
}

variable "domain_name" {
  description = "Custom domain assigned for the URL shortener"
  type        = string
  default     = "group5-urlshortener.sctp-sandbox.com"
}

variable "my_ip" {
  #description = "Your public IP"
  #type         = string
  #default     = "0.0.0.0/32" # UPDATE THIS
  description = "The IP range allowed to access the API. Set to 0.0.0.0/0 to allow global access."
  type        = string
  default     = "0.0.0.0/0"
}
