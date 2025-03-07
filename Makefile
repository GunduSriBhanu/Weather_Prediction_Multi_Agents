PYTHON_VERSION := 3.12.0
PYTHON_TARBALL := Python-$(PYTHON_VERSION).tgz
PYTHON_SRC_DIR := Python-$(PYTHON_VERSION)

install-dev-tools:
	sudo yum groupinstall -y "Development Tools"
	sudo yum install -y gcc libffi-devel bzip2 bzip2-devel zlib-devel xz-devel wget readline-devel sqlite sqlite-devel openssl-devel xz xz-devel

download-python:
	wget https://www.python.org/ftp/python/$(PYTHON_VERSION)/$(PYTHON_TARBALL)
	tar xzf $(PYTHON_TARBALL)

build-python:
	cd $(PYTHON_SRC_DIR) && sudo ./configure --enable-optimizations
	cd $(PYTHON_SRC_DIR) && make
	cd $(PYTHON_SRC_DIR) && sudo make altinstall

verify-installation:
	python3.12 -m ssl

clean:
	rm -rf $(PYTHON_TARBALL) $(PYTHON_SRC_DIR)

help:
	echo "Available Commands"
	echo "  install-dev-tools     Install required development tools"
	echo "  download-python       Download and extract Python $(PYTHON_VERSION)"
	echo "  build-python          Build and install Python $(PYTHON_VERSION)"
	echo "  verify-installation   Verify Python installation"
	echo "  clean                 Remove installation files"
