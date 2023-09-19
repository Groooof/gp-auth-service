import typing as tp
import secrets


IMAGES = ['😂', '😍', '😈', '😎', '😡', '🖤', '👽', '🤖',
          '😅', '👍', '👎', '⭐', '🍋', '⚽', '🇷🇺', '📌',
          '💊', '💲', '🚀', '☕', '🍒', '⚡', '🏈', '🕷',
          '🐼','🥶', '👻', '🦠', '💜', '🌈', '💧', '🦋',
          '⚓', '💎', '💰', '🔒', '🎱', '🍉', '🌶', '🎲',
          '💌', '💡', '📞', '👁', '💋', '💙', '⛔', '✅',
          '🌙', '🍕', '🍄', '🧲', '🔑', '🎁', '🥇', '🍔',
          '🔥', '🍁', '🌹', '🐌', '💣', '😭', '🦴', '🙏']


class GraphicalPasswordManager:
    _images = IMAGES
    
    def __init__(self, size=3) -> None:
        self._size = size
    
    def get_pass_images(self,
                        step_2_choice: str,
                        step_3_choice: str,
                        step_1_imgs: tp.List[tp.List[str]],
                        step_2_imgs: tp.List[tp.List[str]],
                        step_3_imgs: tp.List[tp.List[str]],
                        ) -> str:
        
        step_3_choice_pos = self._find_in_matrix(step_3_imgs,
                                                 step_3_choice)
        step_2_choice_pos = self._find_in_matrix(step_2_imgs,
                                                 step_2_choice)
        
        pwd_1 = step_1_imgs[step_2_choice_pos[0]] \
                           [step_2_choice_pos[1]]
        pwd_2 = step_2_imgs[step_3_choice_pos[0]] \
                           [step_3_choice_pos[1]]
        
        return f'{pwd_1}{pwd_2}'
    
    def get_random_matrix(self):
        temp_images = self._images.copy()
        matrix = []
        for row in range(self._size):
            matrix.append([])
            for _ in range(self._size):
                item = secrets.choice(temp_images)
                matrix[row].append(item)
                temp_images.remove(item)
        return matrix

    def _find_in_matrix(self,
                        matrix: tp.List[tp.List[tp.Any]],
                        value: tp.Any) -> tp.Optional[tp.Tuple[int, int]]:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == value:
                    return i, j
        return None
