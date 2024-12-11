# Instagram Scraping Tool

Este projeto realiza o **scraping** de posts no **Instagram**, coletando informações como curtidas, comentários e outros dados dos usuários utilizando **Selenium** e **WebDriver**.

---

## 📋 Requisitos

Antes de executar o projeto, certifique-se de ter os seguintes pacotes e ferramentas instalados:

- **Python 3.x**: Este projeto é compatível com Python 3.
- **Selenium**: Para automação do navegador.
- **WebDriver Manager**: Para gerenciar o driver do Chrome de forma automática.
- **Python Dotenv**: Para gerenciar variáveis de ambiente de forma segura.

Para instalar as dependências, execute:

```bash
pip install selenium webdriver_manager python-dotenv
```

---

## ⚙️ Configuração

### 1. Crie um arquivo `.env`

No diretório raiz do projeto, crie um arquivo `.env` com suas credenciais do Instagram:

```dotenv
INSTAGRAM_USERNAME=<SEU_USERNAME>
INSTAGRAM_PASSWORD=<SUA_SENHA>
```

> **Aviso**: Não compartilhe seu arquivo `.env` com outras pessoas para manter suas credenciais seguras.

---

## 🚀 Configuração do Driver

### **Linux** (Arch Linux):

1. **Instale o `chromedriver`** em `/usr/bin/chromedriver` ou em outro diretório de sua preferência.

2. O código está configurado para usar o `chromedriver` diretamente:

```python
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service)
print(f"ChromeDriver Version: {driver.capabilities['chrome']['chromedriverVersion']}")
print(f"Browser Version: {driver.capabilities['browserVersion']}")
```

### **Windows**:

No Windows, o código utiliza o **WebDriver Manager** para baixar o `chromedriver` automaticamente:

```python
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

---

## 🎬 Execução

1. Após a configuração do arquivo `.env` e a instalação das dependências, execute o script principal:

```bash
python main.py
```

2. O script fará login no Instagram usando as credenciais fornecidas e realizará as interações configuradas (ex.: coletar informações de curtidas, comentários, etc.).

---

## 🤝 Contribuição

Sinta-se à vontade para contribuir para o projeto! Você pode:

- Reportar bugs
- Sugerir melhorias
- Submeter pull requests

Se você tiver alguma dúvida ou sugestão, crie uma **issue** ou envie um **pull request**.

---

> **Aviso Legal**: Este projeto é para um trabalho acadêmico. Utilize-o de maneira responsável, respeitando as políticas de uso do Instagram e outras plataformas.



---
