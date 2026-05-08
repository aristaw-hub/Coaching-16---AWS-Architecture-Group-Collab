resource "aws_api_gateway_rest_api" "api" {
  name = "group5-url-api"
}

# POST /newurl
resource "aws_api_gateway_resource" "newurl" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "newurl"
}

resource "aws_api_gateway_method" "post_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.newurl.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_int" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.newurl.id
  http_method             = aws_api_gateway_method.post_method.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.create_url.invoke_arn
}

# GET /{shortid}
resource "aws_api_gateway_resource" "geturl" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "{shortid}"
}

resource "aws_api_gateway_method" "get_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.geturl.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_int" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.geturl.id
  http_method             = aws_api_gateway_method.get_method.http_method
  type                    = "AWS"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.retrieve_url.invoke_arn
  request_templates       = { "application/json" = "{\"short_id\": \"$input.params('shortid')\"}" }
}

resource "aws_api_gateway_method_response" "resp_302" {
  rest_api_id         = aws_api_gateway_rest_api.api.id
  resource_id         = aws_api_gateway_resource.geturl.id
  http_method         = aws_api_gateway_method.get_method.http_method
  status_code         = "302"
  response_parameters = { "method.response.header.Location" = true }
}

resource "aws_api_gateway_integration_response" "int_resp" {
  rest_api_id         = aws_api_gateway_rest_api.api.id
  resource_id         = aws_api_gateway_resource.geturl.id
  http_method         = aws_api_gateway_method.get_method.http_method
  status_code         = "302"
  response_parameters = { "method.response.header.Location" = "integration.response.body.location" }
  depends_on          = [aws_api_gateway_integration.get_int]
}

# Domain & Stage
resource "aws_api_gateway_stage" "prod" {
  deployment_id        = aws_api_gateway_deployment.main.id
  rest_api_id          = aws_api_gateway_rest_api.api.id
  stage_name           = "prod"
  xray_tracing_enabled = true
}

resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  depends_on  = [aws_api_gateway_integration.post_int, aws_api_gateway_integration.get_int]
}

resource "aws_api_gateway_domain_name" "custom" {
  domain_name              = var.domain_name
  regional_certificate_arn = data.aws_acm_certificate.cert.arn
  endpoint_configuration { types = ["REGIONAL"] }
}

resource "aws_api_gateway_base_path_mapping" "map" {
  api_id      = aws_api_gateway_rest_api.api.id
  stage_name  = aws_api_gateway_stage.prod.stage_name
  domain_name = aws_api_gateway_domain_name.custom.domain_name
}

resource "aws_route53_record" "dns" {
  name    = var.domain_name
  type    = "A"
  zone_id = data.aws_route53_zone.sctp_zone.zone_id
  alias {
    name                   = aws_api_gateway_domain_name.custom.regional_domain_name
    zone_id                = aws_api_gateway_domain_name.custom.regional_zone_id
    evaluate_target_health = false
  }
}

resource "aws_lambda_permission" "apigw_create" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_url.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "apigw_retrieve" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.retrieve_url.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}
