FROM python:3.11
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz
RUN tar xvf geckodriver-v0.36.0-linux64.tar.gz
RUN rm geckodriver-v0.36.0-linux64.tar.gz
RUN mv geckodriver /usr/bin/
# b-hunters==1.1.16
RUN pip install  b-hunters==1.1.16 wapiti3
RUN wapiti --update
# WORKDIR /app/service
# COPY ./xray/ /xray/
WORKDIR /app/service
COPY wapitim /app/service/wapitim
CMD [ "python", "-m", "wapitim" ]

# ENTRYPOINT [ "/bin/bash" ]