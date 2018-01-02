_PROFILE=airvideoserver-hd
_MODULE=systemdock-$(_PROFILE)
PREFIX = $(DESTDIR)/usr
SYSCONFDIR=$(DESTDIR)/etc
DATADIR=$(PREFIX)/share
SYSTEMD_DIR=$(PREFIX)/lib/systemd/system
INSTALL = /bin/install -c
MKDIR = /bin/install -c -d
RM = rm -rf
CP = cp -a
LN = ln -s
TAR = $(shell which tar)
TMPDIR := $(shell mktemp -d)
CURRENT_DIR := $(shell pwd)
PKG_MGR := $(shell which yum)
RPMBUILD := $(shell which rpmbuild)

install:
	$(MKDIR) $(SYSCONFDIR)/systemdock/containers.d
	$(MKDIR) $(SYSTEMD_DIR)
	$(CP) $(_PROFILE) $(SYSCONFDIR)/systemdock/containers.d
	$(LN) $(SYSCONFDIR)/systemdock/containers.d/$(_PROFILE)/$(_MODULE).service $(SYSTEMD_DIR)/$(_MODULE).service

uninstall:
	$(RM) $(SYSTEMD_DIR)/$(_MODULE).service
	$(RM) $(SYSCONFDIR)/systemdock/containers.d/$(_PROFILE)

rpm:
	$(TAR) \
		cvfz $(TMPDIR)/$(_MODULE).tar.gz \
		--transform 's,^,$(_MODULE)/,' \
	       	--exclude=.git \
		--exclude=.gitignore \
		--exclude='*.swp' \
		--exclude=.rpmbuild \
		--exclude=$(_MODULE).tar.gz \
		./
	mkdir -p .rpmbuild/SPEC .rpmbuild/SOURCES .rpmbuild/SRPMS .rpmbuild/RPMS .rpmbuild/BUILD .rpmbuild/BUILDROOT
	mv $(TMPDIR)/$(_MODULE).tar.gz .rpmbuild/SOURCES
	$(RPMBUILD) -tb --define "_topdir $(CURRENT_DIR)/.rpmbuild" .rpmbuild/SOURCES/$(_MODULE).tar.gz
	$(RPMBUILD) -ta --define "_topdir $(CURRENT_DIR)/.rpmbuild" .rpmbuild/SOURCES/$(_MODULE).tar.gz

install-rpm: rpm
	$(PKG_MGR) install -y .rpmbuild/RPMS/noarch/$(_MODULE)*

uninstall-rpm:
	$(PKG_MGR) remove -y $(_MODULE) || :

reinstall-rpm: uninstall-rpm install-rpm 

clean:
	$(RM) .rpmbuild
