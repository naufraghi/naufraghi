### Set "N" as accelerator for "Next Unread Message" ###

```
diff -u /usr/share/evolution/2.12/ui/evolution-mail-message.xml.orig /usr/share/evolution/2.12/ui/evolution-mail-message.xml
--- /usr/share/evolution/2.12/ui/evolution-mail-message.xml.orig        2007-09-18 14:06:00.000000000 +0200
+++ /usr/share/evolution/2.12/ui/evolution-mail-message.xml     2007-09-18 14:06:35.000000000 +0200
@@ -30,7 +30,7 @@
 
     <cmd name="MailNextUnread"
      _tip="Display the next unread message"
-     accel="*Control*bracketright"/>
+     accel="n"/>
 
     <cmd name="MailNextThread"
      _tip="Display the next thread"/>
```


