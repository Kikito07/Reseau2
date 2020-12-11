# Changes made

- The 7E review pointed out that our code was repetitive so we wrapped the deployement of our pexpect scripts inside functions. It doesn't change the network per see but it improves readability.

- A lot of reviews suggested that we add more communities to our network. Se we added AS-prepend X3, set local-pref to 80 and 3 no-export communities one for each continent. It was easy since we already add prepend X1, prepend X2 and set local-pref to 200

- The reviews 7G pointed that having one anycast server per continent would improve latency so we added one more anycast server to ASIA

- The reviews 7G pointed out that plain text authentication wasn't ideal for OSPF. We though that MD5 authentication wasn't working for OSPF but after futher testing we realised that it was in fact working so we replaced plain text authentication with md5 authentication for OSPF.

- We added a new export filter to the routers directly connected to the servers. The servers don't receive routing information anymore. Instead we added a default gateway to them.

