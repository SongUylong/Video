import { makeProject } from "@motion-canvas/core";

import scene01Intro from "./scenes/scene01-intro?scene";
import scene02GlobalNetwork from "./scenes/scene02-global-network?scene";
import scene03Packets from "./scenes/scene03-packets?scene";
import scene04Http from "./scenes/scene04-http?scene";
import scene05Domain from "./scenes/scene05-domain?scene";
import scene06Dns from "./scenes/scene06-dns?scene";
import scene07Hosting from "./scenes/scene07-hosting?scene";
import scene08Browser from "./scenes/scene08-browser?scene";
import scene09Journey from "./scenes/scene09-journey?scene";
import scene10Outro from "./scenes/scene10-outro?scene";

export default makeProject({
  scenes: [
    scene01Intro,
    scene02GlobalNetwork,
    scene03Packets,
    scene04Http,
    scene05Domain,
    scene06Dns,
    scene07Hosting,
    scene08Browser,
    scene09Journey,
    scene10Outro,
  ],
});
