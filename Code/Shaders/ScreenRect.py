import numpy as np
import moderngl
import pygame


class ScreenRect:
          @staticmethod
          def pygame_rect_to_screen_rect(rect: pygame.Rect, target_surface: pygame.Surface, size: tuple) -> pygame.Rect:
                    w = size[0]
                    h = size[1]

                    return pygame.Rect(((rect.x * 2) - w) + rect.w, ((rect.y * 2) + h) - rect.h, rect.w, rect.h)

          def __init__(self, size, win_size, offset, ctx, program):
                    self.size = size
                    self.win_size = win_size
                    offset = (offset[0] / win_size[0], offset[1] / win_size[1])
                    self.current_w, self.current_h = win_size

                    x = self.size[0] / self.current_w
                    y = self.size[1] / self.current_h
                    self.vertices = [
                              (-x + offset[0], y + offset[1]),
                              (x + offset[0], y + offset[1]),
                              (-x + offset[0], -y + offset[1]),

                              (-x + offset[0], -y + offset[1]),
                              (x + offset[0], y + offset[1]),
                              (x + offset[0], -y + offset[1]),
                    ]
                    self.tex_coords = [
                              (0.0, 1.0),
                              (1.0, 1.0),
                              (0.0, 0.0),

                              (0.0, 0.0),
                              (1.0, 1.0),
                              (1.0, 0.0),
                    ]

                    self.vertices = np.array(self.vertices, dtype=np.float32)
                    self.tex_coords = np.array(self.tex_coords, dtype=np.float32)
                    self.data = np.hstack([self.vertices, self.tex_coords])

                    self.vertex_count = 6

                    self.vbo = ctx.buffer(self.data)

                    try:
                              self.vao = ctx.vertex_array(program, [
                                        (self.vbo, '2f 2f', 'vertexPos', 'vertexTexCoord'),
                              ])
                    except moderngl.error.Error:
                              self.vbo = ctx.buffer(self.vertices)
                              self.vao = ctx.vertex_array(program, [
                                        (self.vbo, '2f', 'vertexPos'),
                              ])

                    self.program = program

          def update_vertices(self):
                    offset = (self.offset[0] / self.win_size[0], self.offset[1] / self.win_size[1])
                    self.current_w, self.current_h = self.win_size

                    x = self.size[0] / self.current_w
                    y = self.size[1] / self.current_h
                    self.vertices = [
                              (-x + offset[0], y + offset[1]),
                              (x + offset[0], y + offset[1]),
                              (-x + offset[0], -y + offset[1]),

                              (-x + offset[0], -y + offset[1]),
                              (x + offset[0], y + offset[1]),
                              (x + offset[0], -y + offset[1]),
                    ]
                    self.tex_coords = [
                              (0.0, 1.0),
                              (1.0, 1.0),
                              (0.0, 0.0),

                              (0.0, 0.0),
                              (1.0, 1.0),
                              (1.0, 0.0),
                    ]

                    self.vertices = np.array(self.vertices, dtype=np.float32)
                    self.tex_coords = np.array(self.tex_coords, dtype=np.float32)
                    self.data = np.hstack([self.vertices, self.tex_coords])

          def update_position(self, new_offset):
                    self.offset = new_offset
                    self.update_vertices()
                    self.vbo.write(self.data)

          def update_size(self, new_size):
                    self.size = new_size
                    self.update_vertices()
                    self.vbo.write(self.data)
