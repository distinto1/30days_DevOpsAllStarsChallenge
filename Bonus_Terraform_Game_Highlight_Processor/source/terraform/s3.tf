resource "aws_s3_bucket" "highlights" {
  bucket = var.s3_bucket_name
  # Enable versioning or encryption if needed
  # versioning {
  #   enabled = true
  # }
  # server_side_encryption_configuration {
  #   rule {
  #     apply_server_side_encryption_by_default {
  #       sse_algorithm = "AES256"
  #     }
  #   }
  # }
}

resource "aws_s3_bucket_policy" "highlights" {
  bucket = aws_s3_bucket.highlights.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { AWS = aws_iam_role.ecs_task_execution_role.arn },
      Action    = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
      Resource  = [
        "${aws_s3_bucket.highlights.arn}/*",
        aws_s3_bucket.highlights.arn
      ]
    }]
  })
}