(defun counsel-pydoc-run(x)
  (with-output-to-temp-buffer "*pydoc*"
    (call-process "python" nil "*pydoc*" t "-m" "pydoc" x)
    ))

(defun counsel-pydoc (arg)
  "Run pydoc with counsel. Run with universal argument to invalidate cache"
  (interactive "P")
  (if arg
      (setq counsel-pydoc-names nil))
  (unless counsel-pydoc-names
    (setq counsel-pydoc-names (process-lines "python" "-m"  "pydoc_utils")))   
  (ivy-read "Pydoc: " counsel-pydoc-names
            :action #'counsel-pydoc-run))

