# XPRun

- 抜本的な再設計（Artifact 構成と一体化？）

- Multi-Processing が Execute なのでわかりにくい。

- Extract や Visualize は別プロセスなので大域変数が使えない

- 並列化への対応は必要だが Execute のみの並列化は不便

- API を提供（スクリプトから XPRun を起動したい）

- 仮想環境を作らなくても済むようにする（No run.sh）

- RQ を跨ぐ Cache への対応（Named Cache？）

- Cache と Data の区別をはっきりさせる

- Unnamed Cache の検索可能性の向上

- exe:… は冗長、Extract/Visualize に引数を渡すことは少ない
