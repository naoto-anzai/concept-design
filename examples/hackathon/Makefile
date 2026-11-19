.PHONY: lint matrix journey api derive open

lint:      ## 概念設計を検査する(C1〜C4、入力の性質、未決事項の突き合わせ)
	python3 tools/lint.py

matrix:    ## 検査して、機能 × 概念の対応表も出す
	python3 tools/lint.py --matrix

journey:   ## ジャーニーの雛形を作る(既にあるファイルは上書きしない)
	python3 tools/derive.py journey

api:       ## API の元表を作る(毎回上書き)
	python3 tools/derive.py api

derive: journey api

open:      ## 未決事項だけを出す
	python3 tools/lint.py | grep '\[OQ\]' || true
