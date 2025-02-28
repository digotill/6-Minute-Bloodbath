#version 330

in vec2 fragmentTexCoord;

out vec4 color;

uniform sampler2D imageTexture;
uniform float u_brightness;
uniform vec3 u_color_filter;

void main() {
    vec4 texColor = texture(imageTexture, fragmentTexCoord);
    vec3 brightColor = texColor.rgb * u_brightness;
    vec3 filteredColor = brightColor * u_color_filter;
    color = vec4(filteredColor, texColor.a);
}