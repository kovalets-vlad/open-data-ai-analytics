# bash

git clone -b feature/GitOps https://github.com/kovalets-vlad/open-data-ai-analytics.git
cd open-data-ai-analytics/infra/terraform

terraform init
terraform plan
terraform apply -auto-approve

# Power shell

ssh azureuser@<IP_ВІРТУАЛКИ>

# ВАЖЛИВО: Перевіряємо, чи закінчив роботу cloud-init

tail -f /var/log/cloud-init-output.log

# Отримати айді argo

sudo kubectl get svc -n argocd argocd-server

# Створити апку в агро

sudo kubectl apply -f application.yaml

# 1. Перевірка нод та подів

sudo kubectl get nodes
sudo kubectl get pods -A

# 2. Дізнаємося порти для входу (NodePort)

sudo kubectl get svc -n argocd  
sudo kubectl get svc -n ai-analytics

# 3. Отримуємо пароль адміна для Argo CD

sudo kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

# Подивитися логи сайту (навіть якщо назва пода змінилася)

sudo kubectl logs -l app=web-app -n ai-analytics --tail=50

# Перезапустити застосунок (примусово перечитати конфіги)

sudo kubectl rollout restart deployment web-deployment -n ai-analytics

# Список контейнерів

sudo docker ps

# Логи бази даних

sudo docker logs equipment_db

# Зайти всередину бази (якщо треба перевірити таблиці)

sudo docker exec -it equipment_db psql -U postgres -d equipment_db

# На твоєму ноуті в папці terraform

terraform destroy -auto-approve
