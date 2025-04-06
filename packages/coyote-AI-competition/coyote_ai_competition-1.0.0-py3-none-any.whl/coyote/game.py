import random

class Game:
    def __init__(self):
        pass
#server
   #Deck-class
   #仮
class Deck:
    def __init__(self):
        #初期条件
        #?→ max→0→×2:103,102,101,100に対応
        self.cards = [-10, -5, -5, 0, 0, 0,
                      1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3,
                      4, 4, 4, 4, 5, 5, 5, 5, 
                      10, 10, 10, 15, 15, 20, 
                      100, 101, 102, 103]
        
        self.cashed_cards = [] #山札に戻すカードを格納するリスト
    
    def shuffle(self):
        print ("Deck shuffled.")
        random.shuffle(self.cards)
    
    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            print("No card left in the deck.")
            random.shuffle(self.cashed_cards) #山札に戻すカードをシャッフルする
            #山札が空になったら、捨て札を山札に追加する
            self.cards = self.cashed_cards.copy()
            self.cashed_cards = []
            return self.cards.pop()
    
    def top_show_card(self):
        if len(self.cards) > 0:
            return self.cards[-1]
        return None
    
    def reset(self):
        self.cards = [-10, -5, -5, 0, 0, 0,
                      1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3,
                      4, 4, 4, 4, 5, 5, 5, 5, 
                      10, 10, 10, 15, 15, 20, 
                      100, 101, 102, 103]
        self.shuffle()

def server_draw_card(deck):
            return deck.draw()

def server_top_show_card(deck):
            return deck.top_show_card()      

    #場のカードの合計値を計算する
def calc_card_sum(self, true_cards):
        card_sum = 0 #初期化
        for card in true_cards:
            card_sum += card
        if(self.is_double_card):
            card_sum *= 2 
            self.is_double_card = False
        print(f"gamesum is {card_sum}")    
        return card_sum 
                                  
def convert_card(self, cards, Is_othersum, deck):
        print (f"cards: {cards}")
        true_cards = sorted(cards, reverse = True) 
        index = 0 
        print(f"Initial true_cards: {true_cards}")
        while index < len(true_cards):
            card = true_cards[index]
            print(f"Card drawn: {card}")

            #?を引いたら次のカードを引き、出た番号のカードと交換する
            #全体の数の計算はラウンドにつき一回

            if(card == 103):
                if Is_othersum:
                    new_card = 0  #他プレイヤーの合計値を計算する場合
                else : 
                    new_card = self.deck.draw()
                    deck.cashed_cards.append(new_card) #103を山札に戻す
                print(f"Drawn new card: {deck.cashed_cards}")    
                print(f"Drawn new card: {new_card}")
                if new_card != None: #103を引いた時にNoneがcardsに含まれていたから
                   true_cards[index] = new_card
                   true_cards = sorted(true_cards,reverse=True) 
                   #もし特殊カードを引いてしまったら処理をもう一度行う
                   continue
                else:
                    self.deck.reset()
                    print("No card left in the deck.") 
                    continue   

            #maxを引いたら、最も大きいカードを0にする      
            elif(card == 102):
                normal_cards = [c for c in true_cards if c < 100] #通常カードを取得
                if len(normal_cards) != 0:
                    max_card = max(c for c in true_cards if c < 100) #最大値を取得
                    max_index = true_cards.index(max_card) #最大値のインデックスを取得
                    true_cards[max_index] = 0 #最大値を0にする
                true_cards[true_cards.index(102)] = 0    
                
            #0(黒背景)を引いたら、ラウンド終了後山札をリセットする        
            elif(card == 101):
                true_cards[index] = 0
                #true_cards = sorted(( card for card in true_cards),reverse=True)
                self.is_shuffle_card = True
            elif(card == 100):
                true_cards[index] = 0
                #true_cards = sorted(( card for card in true_cards),reverse=True)
                self.is_double_card = True
            
            index += 1      
      
        return self.calc_card_sum(true_cards)   #関数の外に合計値を返す      
    


def result(self,data):
        """
        ゲームの結果を送信
        試合数が game_num に達してなければstart_gameに戻る, 達していればエンド
        {
            "room_id": "string"
        }
        """
        room_id = data["room_id"]
        room = self.rooms.get_room(room_id)
        is_game_continue = False
        if room:
            if room.current_game_index < room.game_num:
                is_game_continue = True
                
            #TODO: death_ranking, total_win_numをcoyote実装班からもらう
            death_ranking = [{"player_name": player_data["name"]} for sid, player_data in room.death_players]
            room.players[room.active_players[0][0]]["win_num"] += 1
         
            total_win_num = [{"player_name": player_data["name"], "each_ranking": player_data["win_num"]} for sid, player_data in room.players.items()]
                         

#client  
# clinet-class
         
def client_draw_card(self, data):
        """ カードを引く
                 {
                            "header": "draw_card",
                            "card": card
                        },
         """
        print(f"Drawn card: {data['card']}")
        self.hold_card = data['card']