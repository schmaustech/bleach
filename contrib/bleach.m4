define(`confDOMAIN_NAME', `$m')dnl
MASQUERADE_AS(bleach.schmaustech.com)dnl
dnl Sendmail should rebuild the aliases table - considered dangerous
dnl define(`confAUTO_REBUILD', True)dnl

dnl dont know why I defined this, we haven't define a user db
define(`confUSERDB_SPEC',`')dnl

dnl check that address on rhs of colon in aliase file is ok - default true
define(`confCHECK_ALIASES',`True')dnl

dnl checkpoint the queue for list mailings to prevent duplicates
define(`confCHECKPOINT_INTERVAL',`10')dnl

dnl To stop sendmail loops - 17 is recommended
define(`confMAX_HOP',`17')dnl

dnl make sure mailing list sender also gets sent a copy of the mail
define(`confME_TOO',`True')dnl

dnl send errors to postmaster
dnl define(`confCOPY_ERRORS_TO',`Postmaster')dnl
define(`confCOPY_ERRORS_TO',`mailman')dnl

dnl recommended. RFC goof up can result in no MX records, use an A rec instead
define(`confTRY_NULL_MX_LIST',`True')dnl

dnl queue instead of delivering mail at LA=8
define(`confQUEUE_LA',`8')dnl

dnl refuse SMTP connections at LA=12
define(`confREFUSE_LA',`12')dnl

dnl Ya gotta sit in the queue for at least 30 mins - recommended
define(`confMIN_QUEUE_AGE',`30m')dnl

dnl Give em 5 mins to reply to an initial greeting
define(`confTO_INITIAL',`5m')dnl

dnl Give em 5 mins to respond to helo
define(`confTO_HELO',`5m')dnl

dnl not sure why I did this
define(`confTO_DATABLOCK',`1h')dnl

dnl location of service switch, not really necessary on solaris
define(`confSERVICE_SWITCH_FILE',`/etc/nsswitch.conf')dnl
dnl location of host table
define(`confHOSTS_FILE',`/etc/hosts')dnl

dnl log stuff at level 4
define(`confLOG_LEVEL',`9')dnl
dnl not sure I want this ....
define(`LOCAL_MAILER_FLAGS', `EfSn')dnl

dnl sendmail want alias file to be /etc/aliases
define(`ALIAS_FILE', `/etc/mail/aliases')dnl

dnl future use
define(`UUCP_RELAY',`uunet.uu.edu')dnl

dnl future use
define(`BITNET_RELAY',`mail.unet.umn.edu')dnl

dnl if we make it a relay
define(`RELAY_MAILER',`ether')dnl

dnl keep some host status info - new in 8.8.0
define(`confHOST_STATUS_DIRECTORY',`.hoststatus')dnl

dnl keep the host status info valid for 30 mins - recommended
define(`confTO_HOSTSTATUS',`30m')dnl

dnl wait max 5mins for an initial connection - recommended
define(`confTO_CONNECT',`5m')dnl

dnl wait max 5 mins to talk to get a response from host on
dnl an INITIAL connection - recommended
define(`confTO_ICONNECT',`5m')dnl

dnl don't be messing round here
define(`confPRIVACY_FLAGS',`goaway')dnl

dnl Milter
APPENDDEF(`conf_sendmail_ENVDEF', `-DMILTER')
APPENDDEF(`conf_libmilter_ENVDEF', `-D_FFR_MILTER_ROOT_UNSAFE')

