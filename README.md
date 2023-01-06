## Running Plush Survey APP


### 1. Activate virtual env (one-time set-up)

If my_env folder not exists, run:  `python3 -m venv my_env`  to generate.

Activate virtual environment by running:  `source my_env/bin/activate`

### 2. Initialize database

Run `python init_db.py` to initialize the database, it will clear all recorded data, be careful to use it.

### 3. Run the survey app

Run `python app.py` to run the survey app, then copy http://127.0.0.1:5000/consentPage in brower to enter the survey.

### 4. Save all the data in csv format

Run `python saveData.py`  to download the data into questionAnswer folder

## APP Development log

[x] Add a timer to let the annoatoters know how much time is remaining.
[x] Adding more details to the error message for the users who provided incorrect answers to the control questions. 
[x] Modify the math problem so that incorrect responses are more likely to be near to the correct answer.
[x] Using ngrok to test the survey's mobile user interface. Cannot access the publick url link, but have checked the the UI on mobile phone. 
[x] Make the tweet and exp float so that users can still see them even after scrolling to the bottom of the page.
[x] Add link to download full version of consent form.
[x] Move timmer to the top-right of the screen.
[x] Automatically close the question page when time out.
[x] Add dismissible error message.
[] Separate the tweets into independent survey URLs

## Reading Lists

### Knowledge Base Construction
[x] *Bosselut, Antoine, et al.* [COMET: Commonsense transformers for automatic knowledge graph construction](https://arxiv.org/pdf/1906.05317) ACL'2019 [Slides Link](https://docs.google.com/presentation/d/1uBwNkusg8EPCqyuWJUfMnRB1-sc2gAb5-v11oz5mJzU/edit?usp=sharing)

[x] Robyn Speer, Joshua Chin, and Catherine Havasi.* [Conceptnet 5.5: An open multilingual graph of general knowledge.](https://arxiv.org/pdf/1612.03975.pdf) In Thirty-First AAAI Conference on Artificial Intelligence [Slides Link](https://docs.google.com/presentation/d/1VafO0tqyxLhZFJvExc_Tm1bBvPAkcNHUwLUGoSTKW2E/edit?usp=sharing)

[x] *Maarten Sap, Ronan LeBras, Emily Allaway, Chandra Bhagavatula, Nicholas
Lourie, Hannah Rashkin, Brendan Roof, Noah A Smith, and Yejin Choi.* [Atomic: An atlas of machine commonsense for ifthen reasoning.](https://ojs.aaai.org/index.php/AAAI/article/view/4160) In AAAI. [Slides Link](https://docs.google.com/presentation/d/1VafO0tqyxLhZFJvExc_Tm1bBvPAkcNHUwLUGoSTKW2E/edit?usp=sharing)

[] *Auer, S., Bizer, C., Kobilarov, G., Lehmann, J., Cyganiak, R., & Ives, Z.* [Dbpedia: A nucleus for a web of open data.](https://link.springer.com/content/pdf/10.1007/978-3-540-76298-0_52.pdf) In The semantic web (pp. 722-735). Springer, Berlin, Heidelberg.

[] *Roemmele, M., Bejan, C. A., & Gordon, A. S.* [Choice of Plausible Alternatives: An Evaluation of Commonsense Causal Reasoning.](https://www.researchgate.net/profile/Cosmin-Bejan/publication/221251392_Choice_of_Plausible_Alternatives_An_Evaluation_of_Commonsense_Causal_Reasoning/links/5c129b024585157ac1c05c6e/Choice-of-Plausible-Alternatives-An-Evaluation-of-Commonsense-Causal-Reasoning.pdf) In AAAI spring symposium: logical formalizations of commonsense reasoning (pp. 90-95).

[] *Rashkin, H., Sap, M., Allaway, E., Smith, N. A., & Choi, Y.* [Event2Mind: Commonsense Inference on Events, Intents, and Reactions](https://aclanthology.org/P18-1043.pdf) arXiv preprint arXiv:1805.06939.

~~[] *Chu, C. X., Tandon, N., & Weikum, G.* [Distilling task knowledge from how-to communities.](https://dl.acm.org/doi/pdf/10.1145/3038912.3052715?casa_token=xLX4-dnRg28AAAAA:KqceMVm_XuTnPSDOccMFudl-hMDa7E8XvZ6RU8pwnQ_G72y1XuayHi_pafcoelHbQiBHZpT58Guc) In Proceedings of the 26th International Conference on World Wide Web (pp. 805-814).~~

### Knowledge Base Applcations
[] *Zou, X.* [A survey on application of knowledge graph.* In Journal of Physics: Conference Series](https://iopscience.iop.org/article/10.1088/1742-6596/1487/1/012016/pdf) IOP Publishing.

### Knowledge Base Embeddings
[] Nickel, M., Rosasco, L., & Poggio, T.* [Holographic embeddings of knowledge graphs.](https://arxiv.org/pdf/1510.04935.pdf) In Proceedings of the AAAI Conference on Artificial Intelligence (Vol. 30, No. 1).

### Entity linking
- [DeepType: Multilingual Entity Linking by Neural Type System Evolution](https://arxiv.org/pdf/1802.01021.pdf)
- [Evaluating the Impact of Knowledge Graph Context on Entity Disambiguation Models](https://arxiv.org/pdf/2008.05190.pdf)
