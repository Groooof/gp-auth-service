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
                        step_2_selection: str,
                        step_3_selection: str,
                        step_1_images: tp.List[tp.List[str]],
                        step_2_images: tp.List[tp.List[str]],
                        step_3_images: tp.List[tp.List[str]],
                        ) -> str:
        
        step_3_selection_position = self._get_index_from_matrix(step_3_images, step_3_selection)
        step_2_selection_position = self._get_index_from_matrix(step_2_images, step_2_selection)

        pwd_1 = step_1_images[step_2_selection_position[0]][step_2_selection_position[1]]
        pwd_2 = step_2_images[step_3_selection_position[0]][step_3_selection_position[1]]

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

    def _get_index_from_matrix(self,
                              matrix: tp.List[tp.List[tp.Any]],
                              value: tp.Any) -> tp.Optional[tp.Tuple[int, int]]:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == value:
                    return i, j
        return None
