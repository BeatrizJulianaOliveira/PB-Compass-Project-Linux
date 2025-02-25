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

### 2️⃣ Criação de Security Group
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

### 3️⃣ Provisionamento da Instância EC2

#### Implantação da Instância
1. Acesse o console da AWS e vá até **EC2 > Instances**.  
2. Clique em **Launch Instances** para iniciar o provisionamento.  
3. Selecione a **Amazon Linux 2023 AMI** como sistema operacional da instância.  
4. Defina as tags necessárias e vincule a instância à **VPC configurada anteriormente**, garantindo que ela esteja em uma **sub-rede pública**.  

#### Configuração de Acesso
1. **Gere e associe uma chave SSH (.pem)** para permitir conexões remotas seguras.  
2. Vincule a instância ao **Security Group definido previamente**, assegurando o controle adequado do tráfego de rede.  
3. Finalize a criação da instância clicando em **Launch Instance**.  
### 4️⃣ Conectando-se à Instância EC2 via SSH  

Após o lançamento da instância, é necessário estabelecer uma conexão SSH para realizar as configurações iniciais.  

#### Acesso pelo Visual Studio Code  
1. Acesse o **console da AWS** e vá até **EC2 > Instâncias**.  
2. Selecione a instância desejada e clique em **Connect**.  
3. Copie o comando exibido na seção **SSH Client**.  
4. No **Visual Studio Code**, abra o terminal e cole o comando copiado.  
5. Substitua `"nome_da_chave"` pelo caminho correto do arquivo `.pem`, geralmente localizado em:  
   ```bash
   C:\Users\seu_usuario\.ssh\nome_da_chave.pem

## Etapa 2: Configuração do Servidor Web (Nginx)

### 📌 1. Instalando o Nginx
Para configurar o servidor web, primeiro instale o **Nginx** utilizando o gerenciador de pacotes do **Amazon Linux**:

```bash
sudo yum install nginx -y
```

Após a instalação, verifique se o **Nginx** foi instalado corretamente:

```bash
nginx -v
```

---

### ⚙️ 2. Configurando o Nginx
Agora, inicie o serviço **Nginx** e configure-o para iniciar automaticamente sempre que a instância EC2 for ligada:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

Para garantir que o **Nginx** está em execução, verifique seu status com:

```bash
sudo systemctl status nginx
```

Se tudo estiver correto, ele deve estar **ativo e rodando**. ✅

---

### 🖥️ 3. Criando uma Página Web Simples
Agora, vamos criar uma página HTML básica para testar o servidor.

Abra o arquivo de **index** no editor de texto:

```bash
sudo nano /usr/share/nginx/html/index.html
```

Edite o conteúdo conforme necessário, salve e saia do editor (**CTRL+X → Y → ENTER**).

🔗 **Dica**: A página utilizada neste projeto pode ser encontrada neste repositório.

Para testar, acesse o **IP público** da instância EC2 no navegador. Se tudo estiver certo, a página será exibida corretamente! 🎉

---

### 🔄 4. Configuração para Reinício Automático do Nginx
Caso o **Nginx** falhe ou pare de funcionar, podemos garantir que ele será reiniciado automaticamente.

Abra o arquivo de serviço do **Nginx**:

```bash
sudo nano /etc/systemd/system/multi-user.target.wants/nginx.service
```

Adicione as seguintes linhas dentro da seção `[Service]`:

```ini
Restart=always
RestartSec=30
```

📌 **Explicação:**  
- `Restart=always`: Faz com que o **Nginx** reinicie sempre que ocorrer uma falha.
- `RestartSec=30`: Aguarda **30 segundos** antes de tentar reiniciar.

Após adicionar as configurações, salve e saia do editor.

Para aplicar as mudanças, recarregue o **systemd**:

```bash
sudo systemctl daemon-reload
```

Agora, teste se a reinicialização automática está funcionando simulando uma falha.

1️⃣ Obtenha o **PID** (**Process ID**) do **Nginx**:

```bash
ps aux | grep nginx
```

2️⃣ O **PID** do processo mestre será o número exibido antes de `nginx: master process`.

Agora seu servidor **Nginx** está pronto e mais resiliente! 🚀

