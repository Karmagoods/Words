"""
==========================================================
Word Engine
----------------------------------------------------------

Central language engine for the Words application.

Acts as a bridge between:

- Dictionary APIs
- Datamuse
- NLP services
- AI services
- Games

All pages should use this instead of calling APIs directly.

==========================================================
"""


from typing import Optional, Dict, Any

import streamlit as st



# ==========================================================
# PROVIDERS
# ==========================================================


try:

    from services.dictionary import (
        summarize as dictionary_lookup
    )

except Exception:

    dictionary_lookup = None



try:

    from services.datamuse import (
        profile as datamuse_lookup,
        game_words
    )

except Exception:

    datamuse_lookup = None
    game_words = None



try:

    from services.spacy_service import (

        analyze_text,
        get_tokens,
        get_summary

    )

except Exception:

    analyze_text = None
    get_tokens = None
    get_summary = None





# ==========================================================
# ENGINE
# ==========================================================


class WordEngine:


    def __init__(self):

        self.providers = {

            "dictionary":
                dictionary_lookup,

            "datamuse":
                datamuse_lookup

        }




    # ======================================================
    # MAIN SEARCH
    # ======================================================


    @st.cache_data(
        show_spinner=False
    )
    def search(
            _self,
            word: str
    ) -> Optional[Dict[str, Any]]:


        word = word.strip().lower()


        if not word:

            return None



        result = {


            "word":

                word,


            "definitions":

                [],


            "examples":

                [],


            "synonyms":

                [],


            "antonyms":

                [],


            "related":

                [],


            "rhymes":

                [],


            "sounds_like":

                [],


            "triggers":

                [],


            "metadata":

                {},


            "ipa":

                None,


            "audio":

                None,


            "etymology":

                None,


            "tokens":

                [],


            "statistics":

                {}

        }





        # ==================================================
        # DICTIONARY
        # ==================================================


        if dictionary_lookup:


            try:


                data = dictionary_lookup(word)



                if data:


                    result.update({


                        "definitions":

                            data.get(
                                "definitions",
                                []
                            ),


                        "examples":

                            data.get(
                                "examples",
                                []
                            ),


                        "synonyms":

                            data.get(
                                "synonyms",
                                []
                            ),


                        "antonyms":

                            data.get(
                                "antonyms",
                                []
                            ),


                        "ipa":

                            data.get(
                                "ipa"
                            ),


                        "audio":

                            data.get(
                                "audio"
                            )

                    })



            except Exception:


                pass






        # ==================================================
        # DATAMUSE
        # ==================================================


        if datamuse_lookup:


            try:


                data = datamuse_lookup(word)



                if data:


                    result.update({


                        "related":

                            data.get(
                                "related",
                                []
                            ),



                        "rhymes":

                            data.get(
                                "rhymes",
                                []
                            ),



                        "sounds_like":

                            data.get(
                                "homophones",
                                []
                            ),



                        "triggers":

                            data.get(
                                "related",
                                []
                            ),



                        "metadata":

                            data.get(
                                "metadata",
                                {}
                            )

                    })



            except Exception:


                pass






        # ==================================================
        # NLP
        # ==================================================


        if analyze_text:


            try:


                doc = analyze_text(word)


                result["tokens"] = get_tokens(doc)


                result["statistics"] = get_summary(word)



            except Exception:


                pass





        return result






    # ======================================================
    # SIMPLE HELPERS
    # ======================================================


    def get_definition(
            self,
            word
    ):

        data = self.search(word)

        return data["definitions"] if data else []




    def get_synonyms(
            self,
            word
    ):

        data = self.search(word)

        return data["synonyms"] if data else []




    def get_antonyms(
            self,
            word
    ):

        data = self.search(word)

        return data["antonyms"] if data else []




    def get_related(
            self,
            word
    ):

        data = self.search(word)

        return data["related"] if data else []




    def get_rhymes(
            self,
            word
    ):

        data = self.search(word)

        return data["rhymes"] if data else []




    def get_examples(
            self,
            word
    ):

        data = self.search(word)

        return data["examples"] if data else []





    # ======================================================
    # GAME HELPERS
    # ======================================================


    def get_game_word(
            self,
            pattern="*",
            category="general"
    ):

        """
        Returns a game-ready word.

        Used by:

        - Hangman
        - Word Search
        - Crossword

        Parameters:

        pattern:
            Datamuse spelling pattern

            Examples:
            c????
            a*****
            *ing

        category:
            animal
            science
            nature
            technology
            general

        """

        import random


        if game_words:


            try:


                words = game_words(

                    pattern=pattern,

                    category=category,

                    limit=50

                )


                if words:


                    word = random.choice(words)


                    return {


                        "word":

                            word,


                        "category":

                            category,


                        "length":

                            len(word),


                        "pattern":

                            pattern

                    }



            except Exception:


                pass



        # ------------------------------------------
        # Fallback
        # ------------------------------------------

        return {


            "word":

                "language",


            "category":

                "general",


            "length":

                len("language"),


            "pattern":

                pattern

        }
# ==========================================================
# TEST
# ==========================================================


if __name__ == "__main__":


    engine = WordEngine()



    result = engine.search(
        "elephant"
    )



    from pprint import pprint


    pprint(result)



    print("\nGAME WORD:")


    pprint(
        engine.get_game_word(
            "c????"
        )
    )