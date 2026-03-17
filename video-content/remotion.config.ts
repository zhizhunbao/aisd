import { Config } from '@remotion/cli/config';
import path from 'path';

Config.setPublicDir('public');
Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);

// Webpack aliases — 让 Remotion 的 webpack 能解析跨项目引用
Config.overrideWebpackConfig((currentConfig) => {
  return {
    ...currentConfig,
    resolve: {
      ...currentConfig.resolve,
      alias: {
        ...(currentConfig.resolve?.alias ?? {}),
        '@blocks': path.resolve(process.cwd(), '../video-lego/src/blocks'),
        '@lego': path.resolve(process.cwd(), '../video-lego/src/lib'),
      },
    },
  };
});
