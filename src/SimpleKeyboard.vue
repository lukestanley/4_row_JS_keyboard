<template>
  <div :class="keyboardClass"></div>
</template>
<style>
body,
html {
  background: black;
}
.hg-button {
  flex-grow: unset !important;
  width: 66px !important;
  height: 66px !important;
}

.DISABLED.hg-button.hg-functionBtn.hg-button-space {
  width: 120px;
}
.hg-button-arrowleft,
.hg-button-arrowright,
.hg-button-arrowup,
.hg-button-arrowdown {
  no-width: 50px !important;
  background-color: rgba(57, 73, 126, 0.6) !important;
  flex-grow: unset !important;
}
.letterButton {
  font-size: 142%;
  grid-column: col 3 / span 2;
  grid-row: row 2;
  display: grid;
  grid-gap: 0px;
  grid-template-columns: 1fr 1fr;
  min-width: 50px;
}

.main {
  grid-column: 1 / 3;
  grid-row: 1;
  font-size: 100%;
  text-align: center;
}

.left {
  grid-column: 1;
  grid-row: 2;

  color: darkslateblue;
}

.right {
  grid-column: 2;
  grid-row: 2;

  color: rgb(57, 73, 126);
}
.left,
.right {
  font-size: 70%;
  display: block;
  text-align: center;
}
</style>
<script>
import Keyboard from "simple-keyboard";
import "simple-keyboard/build/css/index.css";
// import swipe from "swipe-keyboard";

function countButtons() {
  for (const layoutName in customLayout) {
    console.log(`Layout: ${layoutName}`);
    const layout = customLayout[layoutName];
    for (let i = 0; i < layout.length; i++) {
      const buttonCount = layout[i].split(" ").length;
      if (buttonCount !== 11) {
        throw new Error(
          `Expected 11 buttons on row ${
            i + 1
          } of layout ${layoutName}, but found ${buttonCount}: ${layout[i]}`
        );
      } else {
        console.log(`  Row ${i + 1}: ${buttonCount} buttons`);
      }
    }
  }
}

function toggleFullscreen(el, fallback) {
  var body = document.body;

  // fullscreen API not supported, use fallback if given
  if (
    !body.requestFullscreen &&
    !body.webkitRequestFullScreen &&
    !body.msRequestFullscreen &&
    !body.mozRequestFullScreen
  ) {
    fallback && fallback();
    return;
  }

  // if NOT already in full screen, go full screen now
  if (
    !document.fullscreenElement &&
    !document.webkitFullscreenElement &&
    !document.msFullscreenElement &&
    !document.mozFullScreenElement
  ) {
    if (el.requestFullscreen) el.requestFullscreen();
    else if (el.msRequestFullscreen) el.msRequestFullscreen();
    else if (el.mozRequestFullScreen) el.mozRequestFullScreen();
    else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
  } else {
    if (document.exitFullscreen) document.exitFullscreen();
    else if (document.msExitFullscreen) document.msExitFullscreen();
    else if (document.mozCancelFullScreen) document.mozCancelFullScreen();
    else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
  }
}

const bottomRow =
  "{fn_left} {ctrl} {alt} {space} {space} , . {arrowleft} {arrowdown} {arrowright} {fn_right}";
const customLayout = {
  default: [
    "q w e r t y u i o p {bksp}", // 11
    "a s d f g h j k l # ~", // 11
    "{shift} z x c v b n m {arrowup} @ {enter}", // 11
    bottomRow,
  ],
  fn_left: [
    "1 2 3 4 5 6 7 8 9 0 {bksp}", // 11
    "- + = ~ G H J K L # ~", //11
    "{shift} {full_screen} X C V a \\ / {arrowup} @ {enter}", //11
    bottomRow,
  ],
  fn_right: [
    '~ ! " £ $ % ^ &amp; ( ) {bksp}', // 10
    "_ + D F G H J * @ ` |", //10
    "{shift} Z X &lt; &gt; ? x y n {arrowup} {enter}", //
    bottomRow,
  ],
  shift: [
    "Q W E R T Y U I O P {bksp}", // 10
    "A S D F G H J K L # <",
    "{shift} Z X C V B N M {arrowup} > {enter}",
    bottomRow.replace(" . ", " ? "),
  ],
};
countButtons();
export default {
  name: "SimpleKeyboard",
  props: {
    keyboardClass: {
      default: "simple-keyboard",
      type: String,
    },
    input: {
      type: String,
    },
    theme: String,
  },
  data: () => ({
    keyboard: null,
  }),
  mounted() {
    this.lb = function (input) {
      const splitted = input.split(",");
      const main = splitted[0];
      const left = splitted[1];
      const right = splitted[2];
      let html = `<div class="letterButton"><div class="main">{MAIN}</div><div class="box left">{LEFT}</div><div class="box right">{RIGHT}</div></div>`;
      return html
        .replace("{MAIN}", main)
        .replace("{LEFT}", left)
        .replace("{RIGHT}", right);
    };

    this.keyboard = new Keyboard({
      onChange: this.onChange,
      onKeyPress: this.onKeyPress,
      theme: this.theme,
      mergeDisplay: true,
      display: {
        "{ctrl}": "ctrl",
        q: this.lb("q,1,!"),
        w: this.lb('w,2,"'),
        e: this.lb("e,3,£"),
        r: this.lb("r,4,$"),
        t: this.lb("t,5,%"),
        y: this.lb("y,6,^"),
        u: this.lb("u,7,&"),
        i: this.lb("i,8,*"),
        o: this.lb("o,9,("),
        p: this.lb("p,0,)"),
        a: this.lb("a,-,_"),
        s: this.lb("s,=,+"),
        d: this.lb("d,~, "),
        //_: this.lb(""),
        "{full_screen}": "&#x26F6;",
        "{shift}": "⇧",
        "{bksp}": "⇦",
        "{fn_left}": "<span style='color:darkslateblue'>fn</span>",
        "{fn_right}": "<span style='color:rgb(57, 73, 126)'>fn</span>",
        "{enter}": "&#9166;",
      },
      layout: customLayout,
    });
  },
  methods: {
    onChange(input) {
      this.$emit("onChange", input);
    },
    onKeyPress(button) {
      this.$emit("onKeyPress", button);

      /**
       * If you want to handle the shift and caps lock buttons
       */
      if (button === "{shift}" || button === "{lock}") {
        this.handleAlt("shift");
      }

      if (button === "{fn_left}") {
        this.handleAlt("fn_left");
      }

      if (button === "{fn_right}") {
        this.handleAlt("fn_right");
      }

      if (button === "{full_screen}") {
        toggleFullscreen(document.body);
      }
    },
    handleAlt(pressed) {
      let currentLayout = this.keyboard.options.layoutName;
      let toggledLayout;
      if (currentLayout === "default") {
        toggledLayout = pressed;
      } else {
        toggledLayout = "default";
      }
      this.keyboard.setOptions({
        layoutName: toggledLayout,
      });
    },
  },
  watch: {
    input(input) {
      this.keyboard.setInput(input);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>