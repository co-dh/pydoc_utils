;;; counsel-pydoc.el --- run pydoc with counsel -*- lexical-binding: t; -*-

;; Copyright (C) 2017 Hao Deng

;; Author: Hao Deng(denghao8888@gmail.com)
;; URL: https://github.com/co-dh/pydoc_utils
;; Keywords: completion, matching
;; Package-Requires: ((emacs "24.3") (swiper "0.9.0"))
;; Version: 1.0.0

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <http://www.gnu.org/licenses/>.

;;; Commentary:

;; Run pydoc with counsel.
;; It use python -m pydoc_utils to generate a list of modules, classes, methods, and functions.
;; It cache the result.  To invalidate the cache after new package installed, run counsel-pydoc with universal arguments.
;;
;; Usage: pip install pydoc_utils

;;; Code:

(require 'swiper)

(defun counsel-pydoc-run(x)
  (with-output-to-temp-buffer "*pydoc*"
    (call-process "python" nil "*pydoc*" t "-m" "pydoc" x)
    ))

;;;###autoload
(defun counsel-pydoc (arg)
  "Run pydoc with counsel.
ARG: Run with universal argument to invalidate cache."
  (interactive "P")
  (if arg
      (setq counsel-pydoc-names nil))
  (unless counsel-pydoc-names
    (setq counsel-pydoc-names (process-lines "python" "-m"  "pydoc_utils")))
  (ivy-read "Pydoc: " counsel-pydoc-names
            :action #'counsel-pydoc-run))

(provide 'counsel-pydoc)
;;; counsel-pydoc.el ends here
