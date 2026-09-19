// Optional Ghostty effect: a static warm halation, like light through smoke.
// No flicker, warping or cursor trails. Only a faint, thresholded halo is
// added around bright glyphs, so text and error colours read true.
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    vec2 px = 1.0 / iResolution.xy;
    vec4 source = texture(iChannel0, uv);
    vec3 halo = vec3(0.0);
    for (int i = 0; i < 8; i++) {
        float angle = float(i) * 0.7853982;
        vec2 offset = vec2(cos(angle), sin(angle)) * px * 2.0;
        halo += texture(iChannel0, clamp(uv + offset, vec2(0.0), vec2(1.0))).rgb;
    }
    halo = max(halo / 8.0 - vec3(0.18), vec3(0.0));
    // Smoke scatters warm: the halo leans toward sodium amber.
    float energy = dot(halo, vec3(0.2126, 0.7152, 0.0722));
    vec3 warm = vec3(1.0, 0.72, 0.42) * energy;
    fragColor = vec4(min(source.rgb + warm * 0.14, vec3(1.0)), source.a);
}
