import { Color, AnyFill, TextStyle, TextCompatibleFill } from "./dataModels";

export function colorToCssString(color: Color): string {
    const [r, g, b, a] = color;
    return `rgba(${r * 255}, ${g * 255}, ${b * 255}, ${a})`;
}

function linearGradientToCssString(
    angleDegrees: number,
    stops: [Color, number][]
): string {
    let stopStrings: string[] = [];

    for (let i = 0; i < stops.length; i++) {
        let color = stops[i][0];
        let position = stops[i][1];
        stopStrings.push(`${colorToCssString(color)} ${position * 100}%`);
    }

    return `linear-gradient(${90 - angleDegrees}deg, ${stopStrings.join(
        ", "
    )})`;
}

function radialGradientToCssString(
    centerX: number,
    centerY: number,
    stops: [Color, number][]
): string {
    let stopStrings: string[] = [];

    for (let i = 0; i < stops.length; i++) {
        let color = stops[i][0];
        let position = stops[i][1];
        stopStrings.push(`${colorToCssString(color)} ${position * 100}%`);
    }

    const centerPosition = `${centerX * 100}% ${centerY * 100}%`;
    return `radial-gradient(circle at ${centerPosition}, ${stopStrings.join(
        ", "
    )})`;
}

export function fillToCss(fill: AnyFill): {
    background: string;
    "backdrop-filter": string;
} {
    let background: string;
    let backdropFilter: string = "none";

    switch (fill.type) {
        // Solid Color
        case "solid":
            background = colorToCssString(fill.color);
            break;

        // Linear Gradient
        //
        // Note: Python already ensures that there are at least two stops, and
        // that the first one is at 0 and the last one is at 1. No need to
        // verify any of that here.
        case "linearGradient":
            background = linearGradientToCssString(
                fill.angleDegrees,
                fill.stops
            );
            break;

        // Radial Gradient
        case "radialGradient":
            background = radialGradientToCssString(
                fill.centerX,
                fill.centerY,
                fill.stops
            );
            break;

        // Image
        case "image":
            const cssUrl = `url('${fill.imageUrl}')`;
            switch (fill.fillMode) {
                case "fit":
                    background = `${cssUrl} center/contain no-repeat`;
                    break;
                case "stretch":
                    background = `${cssUrl} top left / 100% 100%`;
                    break;
                case "zoom":
                    background = `${cssUrl} center/cover no-repeat`;
                    break;
                case "tile":
                    background = `${cssUrl} top left / ${fill.tileSize[0]}rem ${fill.tileSize[1]}rem repeat`;
                    break;
                default:
                    // Invalid fill mode
                    // @ts-ignore
                    throw `Invalid fill mode for image fill: ${fill.type}`;
            }
            break;

        // Frosted Glass
        case "frostedGlass":
            background = colorToCssString(fill.color);
            backdropFilter = `blur(${fill.blurSize}rem)`;
            break;

        default:
            // Invalid fill type
            // @ts-ignore
            throw `Invalid fill type: ${fill.type}`;
    }

    return {
        background: background,
        "backdrop-filter": backdropFilter,
    };
}

export function textfillToCss(fill: TextCompatibleFill): {
    color: string;
    background: string;
    backgroundClip: string;
    textFillColor: string;
} {
    // If no fill is provided, stick to the local text color. This allows
    // the user to have their text automatically adapt to different
    // themes/contexts.
    if (fill === null) {
        return {
            color: "var(--rio-local-text-color)",
            background: "var(--rio-local-text-background)",
            backgroundClip: "var(--rio-local-text-background-clip)",
            textFillColor: "var(--rio-local-text-fill-color)",
        };
    }

    // Color?
    if (Array.isArray(fill)) {
        return {
            color: colorToCssString(fill),
            background: "none",
            backgroundClip: "unset",
            textFillColor: "unset",
        };
    }

    // Solid fill, i.e. also a color
    if (fill.type === "solid") {
        return {
            color: colorToCssString(fill.color),
            background: "none",
            backgroundClip: "unset",
            textFillColor: "unset",
        };
    }

    // Anything else
    return {
        color: "unset",
        background: fillToCss(fill).background,
        // TODO: The `backdrop-filter` in `cssProps` is ignored because it
        // doesn't do what we want. (It isn't clipped to the text, it blurs
        // everything behind the element.) This means FrostedGlassFill
        // doesn't blur the background when used on text.
        backgroundClip: "text",
        textFillColor: "transparent",
    };
}

export function textStyleToCss(
    style: "heading1" | "heading2" | "heading3" | "text" | "dim" | TextStyle
): {
    "font-family": string;
    "font-size": string;
    "font-weight": string;
    "font-style": string;
    "text-decoration": string;
    "text-transform": string;
    color: string;
    background: string;
    "-webkit-background-clip": string;
    "-webkit-text-fill-color": string;
    opacity: string;
} {
    let fontFamily: string;
    let fontSize: string;
    let fontWeight: string;
    let fontStyle: string;
    let textDecorations: string[] = [];
    let textTransform: string;
    let color: string;
    let background: string;
    let backgroundClip: string;
    let textFillColor: string;
    let opacity: string;

    // `Dim` is the same as `text`, just with some opacity
    if (style === "dim") {
        style = "text";
        opacity = "0.4";
    } else {
        opacity = "1";
    }

    // Predefined style from theme
    if (typeof style === "string") {
        let globalPrefix = `var(--rio-global-${style}-`;
        let localPrefix = `var(--rio-local-${style}-`;

        // Text fill
        color = localPrefix + "color)";
        background = localPrefix + "background)";
        backgroundClip = localPrefix + "background-clip)";
        textFillColor = localPrefix + "fill-color)";

        // Font weight. This is local so that buttons can make their label text
        // bold.
        fontWeight = localPrefix + "font-weight)";

        // Others
        fontFamily = globalPrefix + "font-name)";
        fontSize = globalPrefix + "font-size)";
        fontStyle = globalPrefix + "font-style)";
        textDecorations.push(globalPrefix + "text-decoration)");
        textTransform = globalPrefix + "all-caps)";
    }

    // Explicitly defined style
    else {
        fontSize = style.fontSize + "em";
        fontStyle = style.italic ? "italic" : "normal";
        fontWeight = style.fontWeight;

        if (style.underlined) {
            textDecorations.push("underline");
        }

        if (style.strikethrough) {
            textDecorations.push("line-through");
        }

        textTransform = style.allCaps ? "uppercase" : "none";

        // If no font family is provided, stick to the theme's.
        if (style.fontName === null) {
            fontFamily = "inherit";
        } else {
            fontFamily = style.fontName;
        }

        ({ color, background, backgroundClip, textFillColor } = textfillToCss(
            style.fill
        ));
    }

    return {
        "font-family": fontFamily,
        "font-size": fontSize,
        "font-weight": fontWeight,
        "font-style": fontStyle,
        "text-decoration":
            textDecorations.length > 0 ? textDecorations.join(" ") : "none",
        "text-transform": textTransform,
        color: color,
        background: background,
        "-webkit-background-clip": backgroundClip,
        "-webkit-text-fill-color": textFillColor,
        opacity: opacity,
    };
}
