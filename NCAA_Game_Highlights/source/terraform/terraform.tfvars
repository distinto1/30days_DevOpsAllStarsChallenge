# terraform.tfvars
# terraform.tfvars

aws_region                = "us-east-1"
project_name             = "highlight-pipeline-final"
s3_bucket_name           = "ncaaahighlightsfinal"
ecr_repository_name      = "highlight-pipeline2-final"

vpc_id                   = "vpc-xxxxxxxxxxxxxxxxx"
public_subnets           = ["subnet-xxxxxxxxxxxxxxxxx"]
private_subnets          = ["subnet-xxxxxxxxxxxxxxxxx"]
igw_id                   = "igw-xxxxxxxxxxxxxxxxx"
public_route_table_id    = "rtb-xxxxxxxxxxxxxxxxx"
private_route_table_id   = "rtb-xxxxxxxxxxxxxxxxx"

rapidapi_ssm_parameter_arn = "arn:aws:ssm:us-east-1:xxxxxxxxxxxx:parameter/myproject/rapidapi_key"

mediaconvert_endpoint     = "https://your_mediaconvert_endpoint_here.amazonaws.com"
mediaconvert_role_arn     = "" # Leaving the string empty will use the role that is created

retry_count                = 5
retry_delay                = 60