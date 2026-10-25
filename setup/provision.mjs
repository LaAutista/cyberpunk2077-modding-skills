#!/usr/bin/env node
export * from '../skills/cyberpunk2077-modding/scripts/setup/provision.mjs';
import {main} from '../skills/cyberpunk2077-modding/scripts/setup/provision.mjs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main().catch(e=>{console.error(e.message);process.exitCode=1;});
