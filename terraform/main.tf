terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. ECS Cluster
resource "aws_ecs_cluster" "classroom_cluster" {
  name = "classroom-cluster"
}

# 2. IAM Role for Task Execution
resource "aws_iam_role" "agentcore_execution_role" {
  name = "classroom-agentcore-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.agentcore_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# 3. ECS Task Definition (Runs your ECR image)
resource "aws_ecs_task_definition" "classroom_task" {
  family                   = "classroom-assistant-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.agentcore_execution_role.arn

  container_definitions = jsonencode([{
    name      = "classroom-assistant"
    image     = "${var.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.repository_name}:latest"
    essential = true
    portMappings = [{
      containerPort = 8080
      hostPort      = 8080
    }]
  }])
}


# Use the default VPC networks to keep it simple
data "aws_vpc" "default" { default = true }
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Create a Security Group to open port 8080
resource "aws_security_group" "ecs_sg" {
  name   = "classroom-ecs-sg"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Change to your IP if you want it private
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Run the task as a continuous service
resource "aws_ecs_service" "classroom_service" {
  name            = "classroom-assistant-service"
  cluster         = aws_ecs_cluster.classroom_cluster.id
  task_definition = aws_ecs_task_definition.classroom_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}