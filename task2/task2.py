from trie import Trie


class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")
        if pattern == "":
            raise ValueError("pattern cannot be empty")

        count = 0

        def dfs(node, path_chars):
            nonlocal count
            if node.is_end_of_word:
                word = "".join(path_chars)
                if word.endswith(pattern):
                    count += 1
            for ch, child in node.children.items():
                path_chars.append(ch)
                dfs(child, path_chars)
                path_chars.pop()

        dfs(self.root, [])
        return count

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")
        if prefix == "":
            raise ValueError("prefix cannot be empty")

        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    trie.count_words_with_suffix("e") == 1  # apple
    trie.count_words_with_suffix("ion") == 1  # application
    trie.count_words_with_suffix("a") == 1  # banana
    trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    trie.has_prefix("app") == True  # apple, application
    trie.has_prefix("bat") == False
    trie.has_prefix("ban") == True  # banana
    trie.has_prefix("ca") == True  # cat

    print("All tests passed.")
