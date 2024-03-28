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

async function processPackages(filename) {
  try {
    const startTime = Date.now();
    let successCount = 0; // Counter for successful URLs

    const packages = JSON.parse(fs.readFileSync(filename, 'utf8'));
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
      const outputFile = `o_${filename}`;
      fs.writeFileSync(outputFile, output.join('\n'));
      console.log(`Output written to ${outputFile}`);
    } else {
      console.log('No valid GitHub URLs found.');
    }

    const endTime = Date.now();
    const timeRequired = (endTime - startTime) / 1000;
    console.log(`Time required: ${timeRequired} seconds`);
    console.log(`Success count: ${successCount}`); // Display success count
    // write success count to a file
    fs.writeFileSync("success_count.txt", successCount);
  } catch (error) {
    console.error('Error processing packages:', error);
  }
}

// List of input filenames
const inputFiles = ['chunk_3.json']; // Add more file names as needed

// Process packages for each input file
inputFiles.forEach(filename => {
  processPackages(filename);
});


// const all_names = ["../all_splits/chunk_8.json"]; // Add more file names as needed

// async function processAllPackages() {
//   for (const fileName of all_names) {
//     await processPackages(fileName);
//     // await sleep(60000); // Wait for 1 minute before processing the next file
//   }
// }

// processAllPackages();
