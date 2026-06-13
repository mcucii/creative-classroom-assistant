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

resource "aws_ecs_cluster" "ui_cluster" {
  name = "classroom-ui-cluster"
}

resource "aws_iam_role" "ui_execution_role" {
  name = "classroom-ui-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role" "ui_task_role" {
  name = "classroom-ui-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}



resource "aws_iam_role_policy_attachment" "ui_execution" {
  role       = aws_iam_role.ui_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "ui_task" {
  family                   = "classroom-ui-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ui_execution_role.arn
  task_role_arn            = aws_iam_role.ui_task_role.arn 

  container_definitions = jsonencode([{
    name      = "classroom-ui"
    image     = "963649480732.dkr.ecr.eu-central-1.amazonaws.com/classroom-ui:latest"
    essential = true
    portMappings = [{
      containerPort = 8501
      hostPort      = 8501
    }]
    environment = [
      {
        name  = "AGENT_RUNTIME_ARN"
        value = "arn:aws:bedrock-agentcore:eu-central-1:963649480732:runtime/classroom_agent-XAQfz84DXl"
      }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/classroom-ui"
        awslogs-region        = "eu-central-1"
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

data "aws_vpc" "default" { default = true }
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_cloudwatch_log_group" "ui" {
  name              = "/ecs/classroom-ui"
  retention_in_days = 7
}

resource "aws_security_group" "ui_sg" {
  name   = "classroom-ui-sg"
  vpc_id = data.aws_vpc.default.id

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

resource "aws_ecs_service" "ui_service" {
  name            = "classroom-ui-service"
  cluster         = aws_ecs_cluster.ui_cluster.id
  task_definition = aws_ecs_task_definition.ui_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.ui_sg.id]
    assign_public_ip = true
  }
}

resource "aws_iam_role_policy" "ui_agentcore" {
  role = aws_iam_role.ui_task_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["bedrock-agentcore:InvokeAgentRuntime"]
      Resource = "*"
    }]
  })
}

output "instructions" {
  value = "Go to ECS console -> classroom-ui-cluster -> Tasks -> click task -> find Public IP -> open http://PUBLIC_IP:8501"
}

