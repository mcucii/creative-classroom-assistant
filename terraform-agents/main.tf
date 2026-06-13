terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}



provider "aws" {
  region = "eu-central-1"
}


# IAM Role for AgentCore
resource "aws_iam_role" "agent_execution" {
  name = "classroom-agent-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "bedrock-agentcore.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "agent_execution" {
  name = "classroom-BedrockAgentCore-execution-role"
  role = aws_iam_role.agent_execution.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        # allow AgentCore to call Bedrock (Claude)
        Effect   = "Allow"
        Action   = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "*"
      },
      {
        # allow AgentCore to pull your image from ECR
        Effect   = "Allow"
        Action   = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:GetAuthorizationToken"
        ]
        Resource = "*"
      },
      {
        # allow AgentCore to write logs
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}




# AgentCore Runtime

resource "aws_bedrockagentcore_agent_runtime" "classroom_agent" {
  agent_runtime_name = "classroom_agent"
  role_arn           = aws_iam_role.agent_execution.arn

  agent_runtime_artifact {
    container_configuration {
      # your ECR image URL directly — no need to manage ECR in this terraform
      container_uri = "963649480732.dkr.ecr.eu-central-1.amazonaws.com/classroom-assistant:latest"
    }
  }

  network_configuration {
    network_mode = "PUBLIC"
  }

  environment_variables = {
    AWS_REGION         = "eu-central-1"
    AWS_DEFAULT_REGION = "eu-central-1"
    DEPLOY_VERSION     = "3"
  }
}


resource "aws_bedrockagentcore_agent_runtime_endpoint" "classroom_endpoint" {
  agent_runtime_id = aws_bedrockagentcore_agent_runtime.classroom_agent.agent_runtime_id
  name              = "default"
}

output "agent_endpoint_arn" {
  value = aws_bedrockagentcore_agent_runtime_endpoint.classroom_endpoint.agent_runtime_endpoint_arn
}