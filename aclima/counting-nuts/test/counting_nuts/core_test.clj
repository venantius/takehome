(ns counting-nuts.core-test
  (:require [clojure.test :refer :all]
            [counting-nuts.core :refer :all]))

(def test-string "Hello, I like nuts. Do you like nuts? No? Are you sure? Why don't you like nuts? Are you nuts? I like you")

(deftest split-on-whitespace-works
  (is (= (split-on-whitespace "I ate a banana") ["I" "ate" "a" "banana"]))
  (is (= (split-on-whitespace test-string) ["Hello," "I" "like" "nuts." "Do" "you" "like" "nuts?" "No?" "Are" "you" "sure?" "Why" "don't" "you" "like" "nuts?" "Are" "you" "nuts?" "I" "like" "you"])))

(deftest split-by-punctuation-works
  (is (= (split-by-punctuation test-string) '("Hello" "I like nuts" "Do you like nuts" "No" "Are you sure" "Why don't you like nuts" "Are you nuts" "I like you"))))

(deftest get-bigram-vector-works
  (is (= (get-bigram-vector ["Are" "you" "sure"])
         [#{"sure" "you"} #{"Are" "you"}]))
  (is (= (get-bigram-vector ["Why" "don't" "you" "like" "nuts"])
         [#{"nuts" "like"} #{"like" "you"} #{"don't" "you"} #{"Why" "don't"}])))

(deftest bigram-frequency-works
  (is (= (reduce concat (bigram-frequency test-string))
         '(#{"i" "like"} 2 #{"are" "you"} 2 #{"like" "you"} 3 #{"nuts" "like"} 3))))
