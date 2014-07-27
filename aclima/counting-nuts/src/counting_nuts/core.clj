(ns counting-nuts.core
  (:require [clojure.test :refer :all]))

;; ASSUMPTIONS
;; - a non-whitespace symbol will appear only at the end of a word
;; - the list of possible punctuation includes/is limited to
;;      the following: ".,:;!\?"
;; - it is acceptable to keep track of the bi-grams all in lowercase

(defn split-on-whitespace
  "Splits all words on whitespace"
  [x]
  (clojure.string/split x #"\s"))

(defn split-by-punctuation
  "Split a string by any punctuation, and trim any whitespace"
  [x]
  (map clojure.string/trim (clojure.string/split x #"[.,:;!\?]")))

(defn get-bigram-vector
  "Takes a vec of words and returns a vec of bigrams
  with each bigram being a two-word set. In general this gets used
  after a sentence has been split up by punctuation"
  [words]
  (cond (< (count words) 2) nil
        (= (count words) 2) [(set words)]
        :else (conj (get-bigram-vector (rest words))
                    #{(first words) (first (rest words))})))

(defn bigram-frequency
  "Given a string, returns a lazy key-value seq where the keys are bigram sets
  and the values are the number of times that bigram appears (in any order)
  in the input string.

  Ignores all bigrams that only show up once in the input corpus."
  [x]
  (filter #(> (second %) 1)
    (frequencies
      (reduce concat ;; turn our seq of vectors into a seq of bigram-sets
        (map get-bigram-vector
           (map split-on-whitespace
              (split-by-punctuation
                (clojure.string/lower-case x))))))))

(defn answer
  "Pretty-prints bigram-frequency results"
  [x]
  (doseq [bigram (bigram-frequency x)]
    (print (clojure.string/join " " (first bigram)))
    (print ": ")
    (println (second bigram))))
