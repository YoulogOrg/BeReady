.PHONY: png

png:
ifeq ($(strip $(FILE)),)
	$(error 未指定文件名，用法: make png FILE=path/to/file.html)
endif
	node scripts/print-png.mjs "$(FILE)"
