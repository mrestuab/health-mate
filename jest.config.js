module.exports = {  
    collectCoverage: true,  
    collectCoverageFrom: [  
      "src/**/*.{js,jsx}",  
      "!src/index.js", // Jangan sertakan file ini  
      "!src/serviceWorker.js", // Jangan sertakan file ini  
      "!src/reportWebVitals.js", // Jangan sertakan file ini  
    ],  
    coverageReporters: ["text", "lcov"],  
  };  
  