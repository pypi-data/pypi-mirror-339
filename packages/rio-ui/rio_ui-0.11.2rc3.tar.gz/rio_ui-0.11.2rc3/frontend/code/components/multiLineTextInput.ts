import { Debouncer } from "../debouncer";
import { markEventAsHandled } from "../eventHandling";
import { InputBox, InputBoxStyle } from "../inputBox";
import { ComponentBase, DeltaState } from "./componentBase";
import {
    KeyboardFocusableComponent,
    KeyboardFocusableComponentState,
} from "./keyboardFocusableComponent";

export type MultiLineTextInputState = KeyboardFocusableComponentState & {
    _type_: "MultiLineTextInput-builtin";
    text: string;
    label: string;
    accessibility_label: string;
    style: InputBoxStyle;
    is_sensitive: boolean;
    is_valid: boolean;
    auto_adjust_height: boolean;
    reportFocusGain: boolean;
};

export class MultiLineTextInputComponent extends KeyboardFocusableComponent<MultiLineTextInputState> {
    private inputBox: InputBox;
    private onChangeLimiter: Debouncer;

    createElement(): HTMLElement {
        let textarea = document.createElement("textarea");
        this.inputBox = new InputBox({ inputElement: textarea });

        let element = this.inputBox.outerElement;

        // Create a rate-limited function for notifying the backend of changes.
        // This allows reporting changes to the backend in real-time, rather
        // just when losing focus.
        this.onChangeLimiter = new Debouncer({
            callback: (newText: string) => {
                this.state.text = newText;

                this.sendMessageToBackend({
                    type: "change",
                    text: newText,
                });
            },
        });

        // Detect value changes and send them to the backend
        this.inputBox.inputElement.addEventListener("input", () => {
            this.onChangeLimiter.call(this.inputBox.value);
        });

        // Detect focus gain...
        this.inputBox.inputElement.addEventListener("focus", () => {
            if (this.state.reportFocusGain) {
                this.sendMessageToBackend({
                    type: "gainFocus",
                    text: this.inputBox.value,
                });
            }
        });

        // ...and focus loss
        this.inputBox.inputElement.addEventListener("blur", () => {
            this.onChangeLimiter.clear();

            this.state.text = this.inputBox.value;

            this.sendMessageToBackend({
                type: "loseFocus",
                text: this.inputBox.value,
            });
        });

        // Detect `shift+enter` and send it to the backend
        //
        // In addition to notifying the backend, also include the input's
        // current value. This ensures any event handlers actually use the up-to
        // date value.
        this.inputBox.inputElement.addEventListener(
            "keydown",
            (event) => {
                if (event.key === "Enter" && event.shiftKey) {
                    this.state.text = this.inputBox.value;
                    this.sendMessageToBackend({
                        text: this.state.text,
                    });

                    markEventAsHandled(event);
                }
            },
            { capture: true }
        );

        // Eat click events so the element can't be clicked-through
        element.addEventListener("click", (event) => {
            event.stopPropagation();
            event.stopImmediatePropagation();

            // Select the HTML text input
            this.inputBox.focus();
        });

        element.addEventListener("pointerdown", (event) => {
            event.stopPropagation();
            event.stopImmediatePropagation();
        });

        element.addEventListener("pointerup", (event) => {
            event.stopPropagation();
            event.stopImmediatePropagation();
        });

        textarea.addEventListener("input", () => {
            if (this.state.auto_adjust_height) {
                this.fitHeightToText();
            }
        });

        return element;
    }

    updateElement(
        deltaState: DeltaState<MultiLineTextInputState>,
        latentComponents: Set<ComponentBase>
    ): void {
        super.updateElement(deltaState, latentComponents);

        if (deltaState.text !== undefined) {
            this.inputBox.value = deltaState.text;
        }

        if (deltaState.label !== undefined) {
            this.inputBox.label = deltaState.label;
        }

        if (deltaState.accessibility_label !== undefined) {
            this.inputBox.accessibilityLabel = deltaState.accessibility_label;
        }

        if (deltaState.style !== undefined) {
            this.inputBox.style = deltaState.style;
        }

        if (deltaState.is_sensitive !== undefined) {
            this.inputBox.isSensitive = deltaState.is_sensitive;
        }

        if (deltaState.is_valid !== undefined) {
            this.inputBox.isValid = deltaState.is_valid;
        }

        if (deltaState.auto_adjust_height !== undefined) {
            if (deltaState.auto_adjust_height) {
                this.fitHeightToText();
            } else {
                this.inputBox.inputElement.style.removeProperty("height");
            }
        }
    }

    fitHeightToText(): void {
        let textarea = this.inputBox.inputElement;
        textarea.style.minHeight = `${textarea.scrollHeight}px`;
    }

    protected override getElementForKeyboardFocus(): HTMLElement {
        return this.inputBox.inputElement;
    }
}
