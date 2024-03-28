
const fs = require('fs');
const axios = require('axios');

async function getGitHubUrl(packageName) {
  try {
    const response = await axios.get(`https://api.npms.io/v2/package/${encodeURIComponent(packageName)}`);
    const githubUrl = response.data.collected.metadata.links.repository;
    return githubUrl;
  } catch (error) {
    console.error('Error fetching GitHub URL:', error);
    return null;
  }
}

async function processPackages() {
  try {
    const startTime = Date.now();
    let successCount = 0; // Counter for successful URLs

    const packages = JSON.parse(fs.readFileSync('c.json', 'utf8'));
    // 
    const output = [];

    const promises = packages.map(async (packageName) => {
      const githubUrl = await getGitHubUrl(packageName);
      if (githubUrl && githubUrl.startsWith('https://github.com/')) {
        const parts = githubUrl.split('/');
        const owner = parts[3];
        const repo = parts[4];
        output.push(`${packageName} ${owner} ${repo} ${githubUrl}`);
        successCount++; // Increment success count
      }
    });

    await Promise.all(promises);

    if (output.length > 0) {
      fs.writeFileSync('oc.txt', output.join('\n').slice(0, 200));
      console.log('Output written to output.txt');
    } else {
      console.log('No valid GitHub URLs found.');
    }

    const endTime = Date.now();
    const timeRequired = (endTime - startTime) / 1000;
    console.log(`Time required: ${timeRequired} seconds`);
    console.log(`Success count: ${successCount}`); // Display success count
  } catch (error) {
    // Suppress errors
  }
}
processPackages();



// async function processPackages() {
//   try {
//     const startTime = Date.now();
//     let successCount = 0; // Counter for successful URLs

//     const packages = JSON.parse(fs.readFileSync('names.json', 'utf8')).slice(0, 30);
//     const output = [];

//     for (const packageName of packages) {
//       const githubUrl = await getGitHubUrl(packageName);
//       if (githubUrl && githubUrl.startsWith('https://github.com/')) {
//         const parts = githubUrl.split('/');
//         const owner = parts[3];
//         const repo = parts[4];
//         output.push(`${packageName} ${owner} ${repo} ${githubUrl}`);
//         successCount++; // Increment success count
//       }
//     }

//     if (output.length > 0) {
//       fs.writeFileSync('output.txt', output.join('\n'));
//       console.log('Output written to output.txt');
//     } else {
//       console.log('No valid GitHub URLs found.');
//     }

//     const endTime = Date.now();
//     const timeRequired = (endTime - startTime) / 1000;
//     console.log(`Time required: ${timeRequired} seconds`);
//     console.log(`Success count: ${successCount}`); // Display success count
//   } catch (error) {
//     // Suppress errors
//   }
// }

processPackages();
