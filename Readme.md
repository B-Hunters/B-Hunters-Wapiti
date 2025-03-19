# B-Hunters-Wapiti

**This module used for Vulnerability Scanning in [B-Hunters Framework](https://github.com/B-Hunters/B-Hunters) using [xray](https://github.com/chaitin/xray).**


## Requirements

To be able to use all the tools remember to update the environment variables with your API keys in `docker-compose.yml` file as some tools will not work well until you add the API keys.


## Configuration
You Can change modules used for wapiti as you like because it can takes too much time. You can find the available modules at [Modules-Names](https://github.com/wapiti-scanner/wapiti?tab=readme-ov-file#module-names)
## Usage 

**Note: You can use this tool inside [B-hunters-playground](https://github.com/B-Hunters/B-Hunters-playground)**   
To use this tool inside your B-Hunters Instance you can easily use **docker-compose.yml** file after editing `b-hunters.ini` with your configuration.

# 1. **Build local**
Rename docker-compose.example.yml to docker-compose.yml and update environment variables.

```bash
docker compose up -d
```

# 2. **Docker Image**
You can also run using docker image
```bash
docker run -d  -e modules=backup,brute_login_form,cms,cookieflags,crlf,csp,csrf,exec,file,htaccess,htp,http_headers,https_redirect,ldap,log4shell,methods,network_device,nikto,permanentxss,redirect,shellshock,spring4shell,sql,ssl,ssrf,takeover,timesql,upload,wapp,wp_enum,xss,xxe -v $(pwd)/b-hunters.ini:/etc/b-hunters/b-hunters.ini bormaa/b-hunters-wapiti:latest
```

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/bormaa)
