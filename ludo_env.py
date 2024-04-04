import ludopy
import numpy as np
import time
import cv2

g = ludopy.Game()
there_is_a_winner = False

while not there_is_a_winner:
    (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()

    enviroment_image_rgb = g.render_environment() # RGB image of the enviroment
    enviroment_image_bgr = cv2.cvtColor(enviroment_image_rgb, cv2.COLOR_RGB2BGR)
    enviroment_image_bgr = cv2.resize(enviroment_image_bgr, (800,800), interpolation = cv2.INTER_LINEAR)
    cv2.imshow("Enviroment", enviroment_image_bgr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

    if len(move_pieces):
        piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
    else:
        piece_to_move = -1

    _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)
    time.sleep(0.1)

cv2.destroyAllWindows()