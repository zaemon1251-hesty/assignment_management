# interface adapter に属する repository で
# domain を引数に持つメソッドを定義するのは、依存性の逆流を引き起こす（usecaseもだが、その層はビジネスロジックだから自分ルールではセーフ）
# (domain)ReadModelなり、(domain)CommandModel という緩衝材を挟むか、
# 原始的な型の可変長引数で実装するか
# 一旦はそのままでいいか
