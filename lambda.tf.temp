# IAM Role
resource "aws_iam_role" "lambda_exec" {
  name = "group5-lambda-exec-role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Action = "sts:AssumeRole", Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" } }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "xray" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}

resource "aws_iam_policy" "db_access" {
  name = "group5-db-access"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action   = ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:UpdateItem"]
      Effect   = "Allow"
      Resource = aws_dynamodb_table.url_table.arn
    }]
  })
}

resource "aws_iam_role_policy_attachment" "db_attach" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.db_access.arn
}

# Lambda: Create URL
data "archive_file" "create_zip" {
  type        = "zip"
  source_file = "${path.module}/src/create/index.py"
  output_path = "create.zip"
}

resource "aws_lambda_function" "create_url" {
  filename      = "create.zip"
  function_name = "group5-create-url"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.9"
  tracing_config { mode = "Active" }

  environment {
    variables = {
      APP_URL    = "https://${var.domain_name}/"
      MIN_CHAR   = "6"
      MAX_CHAR   = "10"
      REGION_AWS = "ap-southeast-1"
      DB_NAME    = aws_dynamodb_table.url_table.name
    }
  }
}

# Lambda: Retrieve URL
data "archive_file" "retrieve_zip" {
  type        = "zip"
  source_file = "${path.module}/src/retrieve/index.py"
  output_path = "retrieve.zip"
}

resource "aws_lambda_function" "retrieve_url" {
  filename      = "retrieve.zip"
  function_name = "group5-retrieve-url"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.9"
  tracing_config { mode = "Active" }

  environment {
    variables = {
      REGION_AWS = "ap-southeast-1"
      DB_NAME    = aws_dynamodb_table.url_table.name
    }
  }
}
