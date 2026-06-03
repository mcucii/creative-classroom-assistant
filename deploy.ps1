# deploy.ps1
Write-Host "Building image..." -ForegroundColor Yellow
docker build --no-cache -t classroom-assistant .

Write-Host "Tagging..." -ForegroundColor Yellow
docker tag classroom-assistant:latest 963649480732.dkr.ecr.eu-central-1.amazonaws.com/classroom-assistant:latest

Write-Host "Logging into ECR..." -ForegroundColor Yellow
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 963649480732.dkr.ecr.eu-central-1.amazonaws.com

Write-Host "Pushing to ECR..." -ForegroundColor Yellow
docker push 963649480732.dkr.ecr.eu-central-1.amazonaws.com/classroom-assistant:latest

Write-Host "Deploying to ECS..." -ForegroundColor Yellow
aws ecs update-service --cluster classroom-cluster --service classroom-assistant-service --force-new-deployment --region eu-central-1 | Out-Null

Write-Host "Waiting for old task to stop..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host "Waiting for new task to become RUNNING..." -ForegroundColor Yellow
$status = ""
while ($status -ne "RUNNING") {
    Start-Sleep -Seconds 10
    $TASK_ARN = (aws ecs list-tasks --cluster classroom-cluster --region eu-central-1 --query "taskArns[0]" --output text)
    $status = (aws ecs describe-tasks --cluster classroom-cluster --tasks $TASK_ARN --region eu-central-1 --query "tasks[0].lastStatus" --output text)
    Write-Host "Task status: $status" -ForegroundColor Cyan
}

Write-Host "Waiting for network interface to attach..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

$IP = ""
while ($IP -eq "" -or $IP -eq "None") {
    $TASK_ARN = (aws ecs list-tasks --cluster classroom-cluster --region eu-central-1 --query "taskArns[0]" --output text)
    $ENI_ID = (aws ecs describe-tasks --cluster classroom-cluster --tasks $TASK_ARN --region eu-central-1 --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" --output text)
    $IP = (aws ec2 describe-network-interfaces --network-interface-ids $ENI_ID --region eu-central-1 --query "NetworkInterfaces[0].Association.PublicIp" --output text)
    if ($IP -eq "" -or $IP -eq "None") {
        Write-Host "Waiting for IP..." -ForegroundColor Cyan
        Start-Sleep -Seconds 40
    }

    Write-Host "IP: $IP" -ForegroundColor Cyan  
}

Write-Host "DONE - Live at: http://$IP:8501" -ForegroundColor Green