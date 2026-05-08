variable "group_name" {
  default = "group5"
}

variable "domain_name" {
  default = "group5-urlshortener.sctp-sandbox.com"
}

variable "my_ip" {
  description = "Your public IP"
  default     = "0.0.0.0/32" # UPDATE THIS
}
