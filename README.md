# Configuração de Servidor Web com Monitoramento

🚀 **Sobre o Projeto**  
Este projeto faz parte do programa de bolsas da Compass UOL, com foco em **Linux, AWS e automação de processos**. O objetivo é configurar um **servidor web** dentro de uma instância **EC2 na AWS**, garantindo sua **disponibilidade** e implementando um **sistema de monitoramento** para detectar possíveis falhas.

---
## 📌 Tecnologias Utilizadas
### ☁️ Infraestrutura em Nuvem (AWS)
- **Amazon VPC** → Rede isolada com sub-redes públicas e privadas.
- **Amazon EC2** → Instância de máquina virtual para o servidor web.
- **Internet Gateway** → Permite acesso externo às instâncias EC2.
- **Security Groups** → Regras de firewall para controle de tráfego HTTP e SSH.

### 🖥️ Sistema Operacional e Acesso
- **SO da Instância**: Amazon Linux (AMI escolhida).
- **Acesso SSH**: Feito pelo VS Code via *Remote - SSH* ou via terminal local com:
  ```bash
  ssh -i "chave.pem" usuario@ip-da-instancia
  ```
- **Alternativa**: Cliente SSH como PuTTY.

### 🌐 Servidor Web
- **Nginx** → Servidor HTTP para hospedar a página HTML.
- **Systemd** → Configura o Nginx para reiniciar automaticamente.

### 🔍 Monitoramento e Automação
- **Bash ou Python** → Script de monitoramento.
- **Curl (Bash) ou Requests (Python)** → Verifica a disponibilidade do site.
- **Logging** → Logs em `/var/log/monitoramento.log`.
- **Cron/Systemd Timers** → Agendamento a cada minuto.

### 📢 Notificações e Alertas
- **Telegram Bot** → Envia alertas quando o servidor cai.
- **Alternativas**: Discord Webhook ou Slack Webhook.

### 🛠️ Automação e Testes
- **Testes Manuais** → Acessar o site via navegador.
- **Simulação de Falhas** → Parar o Nginx e verificar resposta do monitoramento.

---
## ⚙️ Etapa 1: Configuração do Ambiente na AWS
### 1️⃣ Criar uma VPC com:
✅ 2 sub-redes públicas *(para acesso externo)*.  
✅ 2 sub-redes privadas *(para futuras expansões)*.  
✅ Um Internet Gateway conectado às sub-redes públicas.  

No console da AWS, acesse **VPC** > **Suas VPCs** e configure conforme indicado.

### 🌍 Criação da Internet Gateway
1. No console da AWS, vá até **Internet Gateways**.
2. Clique em **Create Internet Gateway** e forneça um nome.
3. Após a criação, selecione o Internet Gateway.
4. Vá até **Actions** → **Attach to VPC**.
5. Associe o Internet Gateway à VPC criada.

### 🔒 Criação de Security Group
1. No console da AWS, vá até **EC2** > **Security Groups**.
2. Clique em **Create Security Group** e forneça um nome.
3. Configure as **Regras de Entrada (Inbound Rules)**:
   | Porta  | Protocolo | Descrição                      |
   |--------|-----------|--------------------------------|
   | 80     | HTTP      | Permitir acesso à web         |
   | 22     | SSH       | Permitir conexões remotas     |
   *🔹 Dica: Restrinja o acesso SSH ao seu IP para maior segurança.*
4. Configure as **Regras de Saída (Outbound Rules)**:
   - **All Traffic** → Permitir saída para qualquer destino (`0.0.0.0/0`).
5. Clique em **Create Security Group** para finalizar.

---
💡 *Pronto! Agora sua VPC e regras básicas de segurança estão configuradas. Vamos para a próxima etapa!* 🚀
