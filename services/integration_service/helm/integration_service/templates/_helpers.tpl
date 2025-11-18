{{- define "telegram-bot.name" -}}
telegram-bot
{{- end -}}

{{- define "telegram-bot.fullname" -}}
{{ .Release.Name }}-{{ include "telegram-bot.name" . }}
{{- end -}}
