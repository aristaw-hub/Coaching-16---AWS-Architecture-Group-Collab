resource "aws_wafv2_ip_set" "ips" {
  name               = "group5-ip-set"
  scope              = "REGIONAL"
  ip_address_version = "IPV4"
  addresses          = [var.my_ip]
}

resource "aws_wafv2_web_acl" "main" {
  name  = "group5-waf"
  scope = "REGIONAL"
  default_action { block {} }

  rule {
    name     = "WhitelistIP"
    priority = 1
    action { allow {} }
    statement { ip_set_reference_statement { arn = aws_wafv2_ip_set.ips.arn } }
    visibility_config { cloudwatch_metrics_enabled = true, metric_name = "group5-waf-ip", sampled_requests_enabled = true }
  }

  visibility_config { cloudwatch_metrics_enabled = true, metric_name = "group5-waf-main", sampled_requests_enabled = true }
}

resource "aws_wafv2_web_acl_association" "assoc" {
  resource_arn = aws_api_gateway_stage.prod.arn
  web_acl_arn  = aws_wafv2_web_acl.main.arn
}

resource "aws_cloudwatch_log_group" "waf" {
  name = "aws-waf-logs-group5"
  retention_in_days = 7
}

resource "aws_wafv2_web_acl_logging_configuration" "log" {
  log_destination_configs = [aws_cloudwatch_log_group.waf.arn]
  resource_arn            = aws_wafv2_web_acl.main.arn
  logging_filter {
    default_behavior = "DROP"
    filter {
      behavior = "KEEP"
      requirement = "MEETS_ANY"
      condition { action_condition { action = "BLOCK" } }
    }
  }
}
