import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import CodeBlock from '@theme/CodeBlock';
import Heading from '@theme/Heading';

import styles from './index.module.css';

// Examples
const yamlExample = `registers:
  - address: 0x00
    name: Temperature
    symbol: TEMP
    fields:
      - name: Temperature
        symbol: T
        bits: [ 15, 4 ]
        access: [ r ]
        format:
          representation: tc
          unit: "Celsius"`;

const cppExample = `/**
 * @brief R | T | 12-bit, read-only register that stores the most recent temperature conversion results (Read)
 * @returns std::expected<uint16_t, std::error_code> The read value, or error code on failure.
 */
[[nodiscard("Function returns expected which represents success or failure")]]
auto Temperature() -> std::expected<uint16_t, std::error_code> {
  if (const auto read_result = this->Read(0x0); !read_result) [[unlikely]] 
    return std::unexpected(read_result.error());
  else [[likely]]
    this->temp_ = read_result.value();
  return this->temp_ & 0xFFF0 >> 4;
}`;

const pythonExample = `// Generated Python Module
def temperature():
    auto read_result = Read<uint16_t>(0x00);
    if (!read_result) return std::unexpected(read_result.error());
    
    uint16_t value = read_result.value();
    // Masking, shifting, and sign-extension handled automatically
    return sign_extend_12bit( (value & 0xFFF0) >> 4 );`;

const cExample = `// Generated C Source
int16_t Temperature(Device* device) {
    int16_t read_result = device.Read16(0x00);
    
    return read_result >> 4;
}`;

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/tutorial-tmp1075n/intro">
            Generate your first library in 5 min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

function HighlightSection() {
  return (
    <div className={clsx('padding-vert--xl', styles.sectionAlt)}>
      <div className="container">
        {/*<div className="row">*/}
          <div className="col">
            <Heading as="h2">From Datasheet to Driver</Heading>
            <p className="padding-vert--md">
              Stop manually calculating bitmasks. Define your hardware in a
              human-readable <strong>YAML</strong> file, and let ChipLib
              generate production-ready, language-agnostic code.
            </p>
            <p>
              Handle complex register maps, bit-fields, and enums with ease. Create libraries according to your specifications. See the example below for a ChipLib register definition and the corresponding automatically generated C++ code.
            </p>
          {/*</div>*/}
          {/*<div className="col col--6">*/}
             {/* Tabs or side-by-side code blocks showing the transformation */}
             <div style={{marginBottom: '1rem'}}>
                <CodeBlock language="yaml" title="Input: TMP1075N.yaml">{yamlExample}</CodeBlock>
             </div>
             <div>
                <CodeBlock language="cpp" title="Output: TMP1075N.cppm">{cppExample}</CodeBlock>
             </div>
             {/*<div>*/}
             {/*   <CodeBlock language="python" title="Output: TMP1075N.py">{pythonExample}</CodeBlock>*/}
             {/*</div>*/}
             {/*<div>*/}
             {/*   <CodeBlock language="c" title="Output: TMP1075N.h">{cExample}</CodeBlock>*/}
             {/*</div>*/}
          </div>
        {/*</div>*/}
      </div>
    </div>
  );
}

function CommunitySection() {
  return (
    <div className="hero hero--light margin-vert--xl">
      <div className="container text--center">
        <Heading as="h2">The Best Part?</Heading>
        <p className="hero__subtitle">
          Skip straight to generating the libraries you need by leveraging a collection of existing ChipLib files.
        </p>
        <div>
          <Link
            className="button button--primary button--lg"
            // TODO: Update link
            to="https://github.com/TSprech/ChipLib/tree/main">
            Browse the Chip Catalog
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home`}
      description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <CommunitySection />
        <HighlightSection />
      </main>
    </Layout>
  );
}
