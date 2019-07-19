divert (-1)
VERSIONID(`@(#)bleach.mc   1.0 Bleach 07/20/2004')dnl
DOMAIN(schmaustech.com)dnl
OSTYPE(linux)dnl
dnl cause we do mail for lots of sites
FEATURE(use_cw_file)dnl

dnl maquerade envelope and header
FEATURE(allmasquerade)dnl
FEATURE(limited_masquerade)dnl

dnl allow for mailertables
FEATURE(mailertable,`hash -o /etc/mailertable')dnl
dnl allow for virtusertable
FEATURE(virtusertable,`hash -o /etc/virtusertable')dnl

dnl  ######### ANTI-SPAM/RELAYING stuff

dnl let all localhost mail go through
FEATURE(relay_entire_domain)

dnl base relay ing on mx records
FEATURE(relay_based_on_MX)

dnl another way to hammer spammers
FEATURE(access_db, `hash -T<TMPF> /etc/mail/access')

dnl How about a little real-time blacklist ?
dnl FEATURE(rbl)

dnl ####ANTI SPAM / ANTI RELAY stuff

dnl specify some mailers
INPUT_MAIL_FILTER(`mimedefang', `S=unix:/var/spool/MIMEDefang/mimedefang.sock, T=S:5m;R:5m')
MAILER(local)dnl
MAILER(smtp)dnl
LOCAL_CONFIG
dnl  gethostbyname needs a little help so set domain here
Dmbleach.schmaustech.com
