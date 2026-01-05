import {Circle, Node, Img, makeScene2D} from '@motion-canvas/2d';
import {createRef, createSignal, waitFor, easeOutCubic, easeInOutCubic} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const GREEN = '#00ff88';
const RED = '#ff6b6b';
const TEAL = '#4ecdc4';
const YELLOW = '#ffd93d';
const PINK = '#ff66aa';
const ORANGE = '#ffaa00';
const PURPLE = '#a29bfe';
const DARK = '#0a0a1a';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const group = createRef<Node>();

  // Icon positions (vertical layout)
  const icons = [
    {name: 'global-network', color: CYAN, y: -700},
    {name: 'packet', color: ORANGE, y: -450},
    {name: 'http', color: RED, y: -200},
    {name: 'https', color: GREEN, y: 50},
    {name: 'domain', color: PINK, y: 300},
    {name: 'dns', color: PURPLE, y: 550},
    {name: 'cloud-server', color: TEAL, y: 800},
    {name: 'browser', color: YELLOW, y: 1050},
  ];

  const potatoScale = createSignal(1);
  const potatoRotation = createSignal(0);

  view.add(
    <Node ref={group} y={700}>
      {/* Simple background - no grid for performance */}
      
      {/* Icons - simplified, no shadows */}
      {icons.map((icon, i) => (
        <Node key={`icon-${i}`} y={icon.y}>
          <Circle
            width={180}
            height={180}
            fill={'#1a1a3a'}
            stroke={icon.color}
            lineWidth={5}
          />
          <Img
            src={`/asset/${icon.name}.png`}
            width={100}
            height={100}
          />
        </Node>
      ))}

      {/* Potato at the very end - simplified */}
      <Node y={1350} scale={() => potatoScale()} rotation={() => potatoRotation()}>
        <Circle
          width={250}
          height={250}
          fill={'#3a2a1a'}
          stroke={ORANGE}
          lineWidth={6}
        />
        <Img
          src={"/asset/potato.svg"}
          width={180}
          height={180}
        />
      </Node>
    </Node>
  );

  // ===== ANIMATION =====
  // Smooth continuous scroll

  yield* group().position.y(700, 0.25, easeOutCubic);
  yield* group().position.y(450, 0.18, easeInOutCubic);
  yield* group().position.y(200, 0.18, easeInOutCubic);
  yield* group().position.y(-50, 0.18, easeInOutCubic);
  yield* group().position.y(-300, 0.18, easeInOutCubic);
  yield* group().position.y(-550, 0.18, easeInOutCubic);
  yield* group().position.y(-800, 0.18, easeInOutCubic);
  yield* group().position.y(-1050, 0.18, easeInOutCubic);

  // Move to potato
  yield* group().position.y(-1350, 0.25, easeInOutCubic);
  yield* waitFor(0.2);

  // Simple potato wiggle
  yield* potatoRotation(8, 0.1);
  yield* potatoRotation(-8, 0.1);
  yield* potatoRotation(0, 0.08);

  yield* waitFor(0.2);

  // ZOOM INTO POTATO - scale potato itself, not the group
  yield* potatoScale(12, 1.0, easeInOutCubic);

  yield* waitFor(1.5);

  // Fade out
  yield* potatoScale(0, 0.3, easeInOutCubic);
});
