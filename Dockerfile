FROM python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
# The browser driver is only used by wapiti's spider module, which the
# worker does not run.  Its download is therefore not allowed to fail the
# build: a flaky network should not cost the worker its image.
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz \
    && tar xvf geckodriver-v0.36.0-linux64.tar.gz \
    && rm geckodriver-v0.36.0-linux64.tar.gz \
    && mv geckodriver /usr/bin/ \
    || echo "the browser driver is not available; the worker does not use it"
# b-hunters==1.5.1
# The shared class is built from this repository, not from the published
# release: a worker that calls auth_headers(task) against a release that
# does not have it fails inside the scan.  scripts/build_workers.sh passes
# the local wheel; the default is the published release.
ARG B_HUNTERS_WHEEL=b-hunters==1.5.1
RUN pip install  ${B_HUNTERS_WHEEL} wapiti3
RUN wapiti --update
# WORKDIR /app/service
# COPY ./xray/ /xray/
WORKDIR /app/service
COPY wapitim /app/service/wapitim
CMD [ "python", "-m", "wapitim" ]

# ENTRYPOINT [ "/bin/bash" ]